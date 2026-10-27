#!/usr/bin/swift
import AppKit
import AVFoundation
import Foundation
import QuartzCore

struct Cue: Codable {
    let start: Double
    let end: Double
    let text: String
}

struct RenderProps: Codable {
    let source: String
    let startSeconds: Double
    let durationSeconds: Double
    let cues: [Cue]
}

func fail(_ message: String) -> Never {
    FileHandle.standardError.write(Data((message + "\n").utf8))
    exit(1)
}

guard CommandLine.arguments.count == 3 else { fail("usage: render_excerpt.swift PROPS OUTPUT") }
let propsURL = URL(fileURLWithPath: CommandLine.arguments[1])
let outputURL = URL(fileURLWithPath: CommandLine.arguments[2])
let props: RenderProps
do {
    props = try JSONDecoder().decode(RenderProps.self, from: Data(contentsOf: propsURL))
} catch {
    fail("invalid render properties")
}
guard props.durationSeconds > 0, props.durationSeconds <= 180, props.cues.count <= 500 else {
    fail("render properties exceed bounds")
}

let sourceURL = URL(fileURLWithPath: props.source)
let asset = AVURLAsset(url: sourceURL)
let composition = AVMutableComposition()
let sourceRange = CMTimeRange(
    start: CMTime(seconds: props.startSeconds, preferredTimescale: 600),
    duration: CMTime(seconds: props.durationSeconds, preferredTimescale: 600)
)

guard let sourceVideo = asset.tracks(withMediaType: .video).first,
      let videoTrack = composition.addMutableTrack(
        withMediaType: .video,
        preferredTrackID: kCMPersistentTrackID_Invalid
      ) else { fail("video track unavailable") }
do {
    try videoTrack.insertTimeRange(sourceRange, of: sourceVideo, at: .zero)
} catch { fail("video range unavailable") }
videoTrack.preferredTransform = sourceVideo.preferredTransform

if let sourceAudio = asset.tracks(withMediaType: .audio).first,
   let audioTrack = composition.addMutableTrack(
    withMediaType: .audio,
    preferredTrackID: kCMPersistentTrackID_Invalid
   ) {
    do {
        try audioTrack.insertTimeRange(sourceRange, of: sourceAudio, at: .zero)
    } catch { fail("audio range unavailable") }
}

let transformed = sourceVideo.naturalSize.applying(sourceVideo.preferredTransform)
let renderSize = CGSize(width: abs(transformed.width), height: abs(transformed.height))
guard renderSize.width >= 640, renderSize.height >= 360 else { fail("video dimensions are invalid") }

let videoComposition = AVMutableVideoComposition(propertiesOf: composition)
videoComposition.renderSize = renderSize
videoComposition.frameDuration = CMTime(value: 1, timescale: 30)

let parent = CALayer()
parent.frame = CGRect(origin: .zero, size: renderSize)
let videoLayer = CALayer()
videoLayer.frame = parent.frame
parent.addSublayer(videoLayer)
let captionLayer = CALayer()
captionLayer.frame = parent.frame
parent.addSublayer(captionLayer)

let fontSize = max(34.0, min(58.0, Double(renderSize.width) / 33.1))
let font = NSFont(name: "Arial Bold", size: fontSize) ?? NSFont.boldSystemFont(ofSize: fontSize)
let outlineWidth = -2.0
let white = NSColor.white
let gold = NSColor(calibratedRed: 0.96, green: 0.76, blue: 0.25, alpha: 1)
let outline = NSColor.black
let maxLineWidth = renderSize.width - 240
let gap = fontSize * 0.27
let lineHeight = fontSize * 1.18

func attributes(_ color: NSColor) -> [NSAttributedString.Key: Any] {
    return [
        .font: font,
        .foregroundColor: color,
        .strokeColor: outline,
        .strokeWidth: outlineWidth,
    ]
}

func textImage(_ text: String, color: NSColor, size: CGSize) -> CGImage? {
    let scale: CGFloat = 2
    let image = NSImage(size: CGSize(width: size.width * scale, height: size.height * scale))
    image.lockFocus()
    NSGraphicsContext.current?.cgContext.scaleBy(x: scale, y: scale)
    NSAttributedString(string: text, attributes: attributes(color)).draw(
        in: CGRect(origin: .zero, size: size)
    )
    image.unlockFocus()
    var rect = CGRect(origin: .zero, size: image.size)
    return image.cgImage(forProposedRect: &rect, context: nil, hints: nil)
}

func addVisibility(_ layer: CALayer, start: Double, end: Double) {
    let total = props.durationSeconds
    let startPoint = max(0, min(1, start / total))
    let endPoint = max(startPoint, min(1, end / total))
    let before = max(0, startPoint - 0.0001)
    let after = min(1, endPoint + 0.0001)
    let animation = CAKeyframeAnimation(keyPath: "opacity")
    animation.values = [0.0, 0.0, 1.0, 1.0, 0.0, 0.0]
    animation.keyTimes = [0.0, NSNumber(value: before), NSNumber(value: startPoint),
                          NSNumber(value: endPoint), NSNumber(value: after), 1.0]
    animation.beginTime = AVCoreAnimationBeginTimeAtZero
    animation.duration = total
    animation.fillMode = .forwards
    animation.isRemovedOnCompletion = false
    layer.opacity = 0
    layer.add(animation, forKey: "visibility")
}

for cue in props.cues where cue.end > cue.start && cue.start < props.durationSeconds {
    let words = cue.text.split(whereSeparator: { $0.isWhitespace }).map(String.init)
    if words.isEmpty || words.count > 40 { continue }
    let widths = words.map { ceil(NSAttributedString(string: $0, attributes: attributes(white)).size().width) + 4 }
    var lines: [[Int]] = [[]]
    var lineWidths: [CGFloat] = [0]
    for index in words.indices {
        let proposed = lineWidths[lineWidths.count - 1] + (lines[lines.count - 1].isEmpty ? 0 : gap) + widths[index]
        if proposed > maxLineWidth && !lines[lines.count - 1].isEmpty && lines.count < 2 {
            lines.append([index])
            lineWidths.append(widths[index])
        } else {
            lines[lines.count - 1].append(index)
            lineWidths[lineWidths.count - 1] = proposed
        }
    }
    let cueStart = max(0, cue.start)
    let cueEnd = min(props.durationSeconds, cue.end)
    let wordSpan = (cueEnd - cueStart) / Double(words.count)
    let blockHeight = CGFloat(lines.count) * lineHeight
    let bottom: CGFloat = 170
    for (lineNumber, indexes) in lines.enumerated() {
        var x = (renderSize.width - lineWidths[lineNumber]) / 2
        let y = bottom + CGFloat(lines.count - lineNumber - 1) * lineHeight
        for index in indexes {
            let frame = CGRect(x: x, y: y, width: widths[index], height: lineHeight)
            let base = CALayer()
            base.frame = frame
            base.contents = textImage(words[index], color: white, size: frame.size)
            base.contentsGravity = .resizeAspect
            addVisibility(base, start: cueStart, end: cueEnd)
            captionLayer.addSublayer(base)

            let active = CALayer()
            active.frame = frame
            active.contents = textImage(words[index], color: gold, size: frame.size)
            active.contentsGravity = .resizeAspect
            let activeStart = cueStart + Double(index) * wordSpan
            addVisibility(active, start: activeStart, end: min(cueEnd, activeStart + wordSpan))
            captionLayer.addSublayer(active)
            x += widths[index] + gap
        }
    }
}

videoComposition.animationTool = AVVideoCompositionCoreAnimationTool(
    postProcessingAsVideoLayer: videoLayer,
    in: parent
)

try? FileManager.default.removeItem(at: outputURL)
guard let exporter = AVAssetExportSession(asset: composition, presetName: AVAssetExportPresetHighestQuality) else {
    fail("export session unavailable")
}
exporter.outputURL = outputURL
exporter.outputFileType = .mp4
exporter.shouldOptimizeForNetworkUse = true
exporter.videoComposition = videoComposition
let semaphore = DispatchSemaphore(value: 0)
exporter.exportAsynchronously { semaphore.signal() }
semaphore.wait()
guard exporter.status == .completed else {
    fail("render failed: \(exporter.error?.localizedDescription ?? "unknown export failure")")
}
