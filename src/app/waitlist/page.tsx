import { HeaderComponent } from "@/components/header-component";
import { CodeBracketsIcon, MenuIcon } from "@/components/leader-board";
import { Button } from "@/components/ui/button";
import { SheetTrigger, SheetContent, Sheet } from "@/components/ui/sheet";
import WaitListComponents from "@/components/wait-list-components";
import Link from "next/link";







export default function WaitList(){
    return (
        <div>
            <header className="flex h-16 items-center justify-between px-4 md:px-6 border-b">
      <Link className="flex items-center gap-2" href="/">
      <CodeBracketsIcon className="h-6 w-6" />
      <span className="font-bold">OMNI-EPIC</span>
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
            <Link href="/waitlist">Waitlist (coming soon)</Link>
          </div>
        </SheetContent>
      </Sheet>
    </header>
       
        <div className="flex min-h-[100dvh] flex-col items-center justify-center px-4 md:px-6">
       
       <WaitListComponents/>
    </div> </div>
    )
}