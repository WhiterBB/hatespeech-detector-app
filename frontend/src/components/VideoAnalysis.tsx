import React from "react";
import ReactPlayer from "react-player";

type HateSegment = {
    start: number;
    end: number;
    score: number;
    label: string;
};

type VideoAnalysisProps = {
    hateSegments: HateSegment[];
    videoDuration: number;
    setVideoDuration: (d: number) => void;
    playerRef: React.RefObject<ReactPlayer | null>;
};

const VideoAnalysis: React.FC<VideoAnalysisProps> = ({
    hateSegments,
    videoDuration,
    playerRef,
}) => {
    const formatTime = (seconds: number): string => {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, "0")}`;
    };

    const handleProgressClick = (time: number) => {
        if (playerRef.current) {
            playerRef.current.seekTo(time, "seconds");
        }
    };

    const hateDuration = hateSegments.reduce(
        (acc, seg) => acc + (seg.end - seg.start),
        0
    );

    const hateCoverage = hateDuration / (videoDuration || 1);
    const avgConfidence =
        hateSegments.reduce((acc, seg) => acc + seg.score, 0) /
        (hateSegments.length || 1);

    return (
        <div className="mt-8">
            <div className="text-center">
                <h2 className="text-xl font-semibold">Video Analysis</h2>
                <p className="text-lg mt-2">
                    🟥 <strong>{(hateCoverage * 100).toFixed(1)}%</strong> of the video contains hate speech
                </p>
                <p className="text-sm text-gray-400">
                    Model average confidence: {(avgConfidence * 100).toFixed(1)}%
                </p>
            </div>

            <div className="relative w-full h-4 bg-gray-300 rounded mt-6 mb-4">
                {hateSegments.map((seg, index) => (
                    <div
                        key={index}
                        className="absolute top-0 h-full bg-red-600"
                        style={{
                            left: `${(seg.start / videoDuration) * 100}%`,
                            width: `${((seg.end - seg.start) / videoDuration) * 100}%`,
                            cursor: "pointer",
                        }}
                        onClick={() => handleProgressClick(seg.start)}
                        title={`${formatTime(seg.start)}–${formatTime(seg.end)} (${(
                            seg.score * 100
                        ).toFixed(0)}%)`}
                    />
                ))}
            </div>

            <div className="mt-4">
                <h3 className="font-bold text-lg mb-2">Detected segments:</h3>
                <ul className="space-y-2">
                    {hateSegments.map((seg, i) => (
                        <li key={i} className="bg-gray-600 p-2 rounded shadow text-sm">
                            <strong>
                                {formatTime(seg.start)} – {formatTime(seg.end)}:
                            </strong>{" "}
                            "{seg.label}" ({(seg.score * 100).toFixed(1)}%)
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default VideoAnalysis;
