import { SocketIdentifier } from "@/app/KeyIdentifier";
import Link from "next/link";

export function HomePage() {
  return (
    <div className="flex flex-col h-screen w-full">
      <main className="flex flex-1 w-full flex-col items-center justify-center p-4">
        <div className="flex w-full max-w-7xl flex-col items-center justify-center gap-4">
          <div id="game-interface" className="aspect-[16/9] w-full overflow-hidden rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold mb-4">Game Interface (for human players!)</h2>
            <p className="text-gray-900 dark:text-gray-400 font-bold">Be one of the first to dive into our interface. Sign up for a <Link href="/waitlist" className="text-purple-500 underline">timeslot</Link> and receive your unique access code.</p>
            <p className="text-gray-900 dark:text-gray-400">The game&apos;s resolution is optimized for smoother and faster rendering.</p>
            {/* <video className="w-full h-full object-cover rounded-md bg-gray-100 dark:bg-gray-800" controls> */}
            <img src="https://app.p2w.app/video_feed" alt="Game Stream"  className="w-full h-full border-rad object-cover rounded-md bg-gray-100 dark:bg-gray-800" />
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