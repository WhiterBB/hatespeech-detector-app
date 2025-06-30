import React from "react";
import ReactPlayer from "react-player";

type VideoPlayerFrameProps = {
  videoUrl: string | null;
  loading: boolean;
  onUpload: (file: File) => void;
  onDuration: (duration: number) => void;
  playerRef: React.RefObject<ReactPlayer | null>;
};

const VideoPlayerFrame: React.FC<VideoPlayerFrameProps> = ({
  videoUrl,
  loading,
  onUpload,
  onDuration,
  playerRef,
}) => {
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) onUpload(file);
  };

  return (
    <div className="relative w-full max-w-4xl aspect-video mx-auto rounded-xl border-2 border-pink-300 bg-gray-800 overflow-hidden shadow-2xl">
      <div className="absolute inset-0 backdrop-blur-md bg-black/20 z-0" />

      {!videoUrl && !loading && (
        <div className="absolute inset-0 flex items-center justify-center z-10">
          <label className="bg-fuchsia-400 hover:bg-fuchsia-700 text-white font-bold py-2 px-6 rounded cursor-pointer shadow-lg">
            Upload video
            <input
              type="file"
              accept="video/*"
              onChange={handleFileChange}
              className="hidden"
            />
          </label>
        </div>
      )}

      {loading && (
        <div className="flex flex-col items-center justify-center gap-4 h-[360px]">
          <svg
            className="animate-spin h-14 w-14 text-pink-500"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
            />
          </svg>
          <p className="text-pink-300 font-semibold text-lg text-center drop-shadow-md">
            Processing video... Please wait.
          </p>
        </div>
      )}

      {videoUrl && !loading && (
        <ReactPlayer
          ref={playerRef}
          url={videoUrl}
          controls
          width="100%"
          height="100%"
          onDuration={onDuration}
          className="absolute top-0 left-0"
        />
      )}
    </div>
  );
};

export default VideoPlayerFrame;
