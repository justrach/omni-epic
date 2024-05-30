import { SocketIdentifier } from "@/app/KeyIdentifier";
import Link from "next/link";

export function HomePage() {
  return (
    <div className="flex flex-col h-screen w-full">
      <main className="flex flex-1 w-full flex-col items-center justify-center p-4">
        <div className="flex w-full max-w-7xl flex-col items-center justify-center gap-4">
          <div id="game-interface" className="aspect-[16/9] w-full overflow-hidden rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold mb-4">Game Interface (coming soon!)</h2>
            {/* <video className="w-full h-full object-cover rounded-md bg-gray-100 dark:bg-gray-800" controls> */}
            <img src="http://localhost:3005/video_feed" alt="Game Stream"  className="w-full h-full border-rad object-cover rounded-md bg-gray-100 dark:bg-gray-800" />
            {/* <img src="/placeholder.svg" alt="Game Stream"  className="w-full h-full border-rad object-cover rounded-md bg-gray-100 dark:bg-gray-800" /> */}
              Your browser does not support the video tag.
            {/* </video> */}
          </div>
          <SocketIdentifier></SocketIdentifier>
          {/* <div className="grid w-full gap-4">
            <h2 className="text-3xl font-bold">Try to beat the leaderboard</h2>
            <h3 className="text-2xl font-medium">The keys that you can use are WASD</h3>
          </div> */}
        </div>
      </main>
   
    </div>
  )
}