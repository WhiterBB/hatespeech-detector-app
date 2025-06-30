import React, { useState, useRef } from "react";
import axios from "axios";
import ReactPlayer from "react-player";
import VideoPlayerFrame from "./components/VideoPlayerFrame";
import VideoAnalysis from "./components/VideoAnalysis";
import "@fontsource/orbitron/700.css";
import "@fontsource/space-grotesk/700.css";

const BASE_URL = import.meta.env.VITE_API_URL;

type HateSegment = {
  start: number;
  end: number;
  score: number;
  label: string;
};

const App: React.FC = () => {
  const [videoURL, setVideoURL] = useState<string | null>(null);
  const [segments, setSegments] = useState<HateSegment[]>([]);
  const [loading, setLoading] = useState(false);
  const [videoDuration, setVideoDuration] = useState<number>(0);
  const playerRef = useRef<ReactPlayer | null>(null);

  const handleUpload = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const response = await axios.post(`${BASE_URL}/analyze`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const allSegments = response.data.data;
      const hateSegments = allSegments.filter(
        (seg: any) => seg.class_predicted === "hate"
      );

      const mappedSegments: HateSegment[] = hateSegments.map((seg: any) => ({
        start: seg.start,
        end: seg.end,
        score: seg.probability,
        label: seg.text,
      }));

      setVideoURL(URL.createObjectURL(file));
      setSegments(mappedSegments);
    } catch (error) {
      console.error("Error analyzing the video", error);
      alert("An error occurred while analyzing the video.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <section className="relative w-full flex flex-col items-center mt-8 mb-6 px-4 sm:px-0">
        <div className="relative w-full flex justify-center mt-8">
          <div className="relative inline-block overflow-hidden w-full max-w-2xl">
        <div className="scanline absolute inset-0 w-full h-full z-20 pointer-events-none"></div>
        <h1
          className="fade-stabilize font-orbitron text-4xl sm:text-6xl md:text-7xl mb-6 text-white tracking-widest relative z-30 text-center"
          data-text="H 8 L E S S"
        >
          H 8 L E S S
        </h1>
          </div>
        </div>

        <div className="flex justify-center w-full">
          <h2 className="typewriter-loop font-space text-base sm:text-lg md:text-xl mb-4 tracking-wide text-gray-300 text-center w-full max-w-xl">
        Less hate, More signal
          </h2>
        </div>
      </section>

      <div className="p-6 max-w-3xl mx-auto">
        <VideoPlayerFrame
          videoUrl={videoURL}
          loading={loading}
          onUpload={handleUpload}
          onDuration={(d) => setVideoDuration(d)}
          playerRef={playerRef}
        />

        {videoURL && segments.length > 0 && (
          <VideoAnalysis
            hateSegments={segments}
            videoDuration={videoDuration}
            setVideoDuration={setVideoDuration}
            playerRef={playerRef}
          />
        )}
      </div>
    </>
  );
};

export default App;
