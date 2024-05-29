"use client"
import { format } from "date-fns";
import { Calendar as CalendarIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { useState } from "react";
import { motion } from "framer-motion";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogTitle } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import Loading from "./loading";

export default function WaitListPage() {
  const [selectedDate, setSelectedDate] = useState<Date>();
  const [timeSlots, setTimeSlots] = useState<any[]>([]);
  const [selectedSlot, setSelectedSlot] = useState<any>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [authCode, setAuthCode] = useState("");

  const [isLoading, setIsLoading] = useState(false);

  const fetchTimeSlots = async (date: Date) => {
    setIsLoading(true); // Set isLoading to true before fetching time slots
    const formattedDate = format(date, "yyyy-MM-dd");
    console.log(`Fetching time slots for date: ${formattedDate}`);
    const response = await fetch(`api/timeslots?date=${formattedDate}`, {
      cache: 'no-store'
    });
    const data = await response.json();
    console.log('Fetched time slots:', data);
    setTimeSlots(data);
    setIsLoading(false); // Set isLoading to false after fetching time slots
  };



  

  const handleDateChange = (date: Date | undefined) => {
    // console.log('Selected date:', date);
    setSelectedDate(date);
    if (date) {
      fetchTimeSlots(date);
    }
  };

  const handleSlotClick = (slot: any) => {
    // console.log('Selected slot:', slot);
    setSelectedSlot(slot);
    setIsDialogOpen(true);
  };

  // console.log(timeSlots, "time slots")
  const handleBookSlot = async () => {
    try {
      // console.log('Booking slot:', selectedSlot);
      const response = await fetch('/api/bookSlots', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          slotId: selectedSlot.id,
          username,
          email,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        // console.log('Booking successful, access token:', data.accessToken);
        setAuthCode(data.accessToken);
        if (selectedDate) {
          fetchTimeSlots(selectedDate);
        }
        setIsDialogOpen(false);
      } else {
        console.log('Booking failed.');
      }
    } catch (error) {
      console.log('Error booking slot:', error);
    }
  };

  return (
    <div className="flex flex-col items-center gap-8 max-w-4xl mx-auto p-4 sm:p-6">
      <h1 className="text-2xl font-bold text-center">Waitlist (book time to play)</h1>
      <div className="flex justify-center">
        <Popover>
          <PopoverTrigger asChild>
            <Button
              variant={"outline"}
              className={cn(
                "w-[280px] justify-center text-center font-normal",
                !selectedDate && "text-muted-foreground"
              )}
            >
              <CalendarIcon className="mr-2 h-4 w-4" />
              {selectedDate ? format(selectedDate, "PPP") : <span>Pick a date</span>}
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-auto p-0">
            <Calendar mode="single" selected={selectedDate} onSelect={handleDateChange} initialFocus />
          </PopoverContent>
        </Popover>
      </div>
      {isLoading ? (
        <Loading /> ): (
      <TimeSlots slots={timeSlots} onSlotClick={handleSlotClick} />)}


      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent>
          <DialogTitle>Book Time Slot</DialogTitle>
          <DialogDescription>
            Please enter your username and email to book the selected time slot.
          </DialogDescription>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input id="username" value={username} onChange={(e) => setUsername(e.target.value)} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            </div>
            <Button onClick={handleBookSlot}>Book</Button>
          </div>
          <DialogFooter></DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}

function TimeSlots({ slots, onSlotClick }: { slots: any[]; onSlotClick: (slot: any) => void }) {
  const timeSlots = generateTimeSlots();

  const fadeInVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { duration: 0.5, staggerChildren: 0.1 } },
  };

  return (
    <motion.div
      className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
      variants={fadeInVariants}
      initial="hidden"
      animate="visible"
    >
      {timeSlots.map((slot) => {
        const bookedSlot = slots.find((bookedSlot) => {
          const bookedStart = format(new Date(bookedSlot.start_time), "HH:mm");
          const bookedEnd = format(new Date(bookedSlot.end_time), "HH:mm");
          return bookedStart === slot.start && bookedEnd === slot.end;
        });

        const isBooked = bookedSlot ? bookedSlot.is_booked : false;

        return (
          <motion.div key={slot.start} variants={fadeInVariants}>
            <Button
              className={`py-2 ${isBooked ? "bg-black text-white" : "bg-white text-black"}`}
              variant="outline"
              onClick={() => onSlotClick(bookedSlot || slot)}
              disabled={isBooked}
            >
              {slot.label}
            </Button>
          </motion.div>
        );
      })}
    </motion.div>
  );
}
function generateTimeSlots() {
  const timeSlots = [];
  let hour = 0;
  let minute = 0;

  while (hour < 24) {
    const start = `${padZero(hour)}:${padZero(minute)}`;
    minute += 10;
    if (minute === 60) {
      hour += 1;
      minute = 0;
    }
    const end = `${padZero(hour)}:${padZero(minute)}`;
    const label = `${start} - ${end}`;
    const isBooked = false;
    timeSlots.push({ start, end, label , isBooked});
  }

  return timeSlots;
}

function padZero(value: number) {
  return value.toString().padStart(2, "0");
}

function formatTime(dateString: string) {
  const date = new Date(dateString);
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}


