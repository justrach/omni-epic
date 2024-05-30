import { AcademicPage } from "@/components/academic_page_v2/acad-page_2";
import { HeaderComponent } from "@/components/header-component";
import { HomePage } from "@/components/home-page";
import { Button } from "@/components/ui/button";
import Link from "next/link"
import { SheetTrigger, SheetContent, Sheet } from "@/components/ui/sheet"
import { Label } from "@/components/ui/label"
import { DropdownMenuTrigger, DropdownMenuRadioItem, DropdownMenuRadioGroup, DropdownMenuContent, DropdownMenu } from "@/components/ui/dropdown-menu"
import { TableHead, TableRow, TableHeader, TableCell, TableBody, Table } from "@/components/ui/table"
import { AvatarImage, AvatarFallback, Avatar } from "@/components/ui/avatar"
import { MenuIcon, CodeBracketsIcon } from "@/components/leader-board";
import TypingAnimation from "@/components/magicui/typing-animation";


export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
    <header className="flex items-center justify-between px-4 py-4 md:px-6 border-b">
       <Link className="flex items-center gap-2" href="/">
      <CodeBracketsIcon className="h-6 w-6" />
      <span className="font-bold"><TypingAnimation   text="OMNI-EPIC"/> </span>
      </Link>
      <Sheet>
        <SheetTrigger asChild>
          <Button size="icon" variant="outline">
            <MenuIcon className="h-6 w-6" />
            <span className="sr-only">Toggle navigation menu</span>
          </Button>
        </SheetTrigger>
        <SheetContent side="right">
          <div className="grid gap-4 p-4">
            <Link href="/">Home</Link>
            <Link href="/waitlist">Waitlist</Link>
          </div>
        </SheetContent>
      </Sheet>
    </header>
     <main className="flex-grow">
    <section className="bg-gray-100 dark:bg-gray-800 py-12 md:py-20">
      <HeaderComponent></HeaderComponent>
    </section>
    <AcademicPage></AcademicPage>
    <HomePage></HomePage>
    </main>
  </div>
  );
}

// export default function WaitPage() {
//   return (
//     <div className="flex min-h-[100dvh] flex-col items-center justify-center px-4 md:px-6">
//       <div className="max-w-md space-y-4 text-center">
//         <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">Research website for OMNI-EPIC coming soon!</h1>
//         <p className="text-gray-500 dark:text-gray-400 md:text-xl">
//       Coming soon!
//         </p>
//       </div>
//     </div>
//   )
// }