// app/api/timeslots/route.ts
import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const dateParam = searchParams.get("date");

  if (!dateParam) {
    return NextResponse.json({ error: "Date parameter is required." }, { status: 400 });
  }
  console.log("Fetching time slots from:", "apiUrl");
  const apiUrl = `https://api.boopr.xyz/slots?date=${dateParam}`;

  try {
    // console.log("Fetching time slots from:", apiUrl);
    // console.log(process.env.BOOPR_API_KEY)
    const response = await fetch(apiUrl, {
      headers: {
        'Authorization': `Bearer ${process.env.BOOPR_API_KEY}`
      },
      cache: 'no-store'
    });
    // console.log(response)
    const data = await response.json();
    // console.log(data)
    return NextResponse.json(data);
  } catch (error) {
    console.error("Error fetching time slots:", error);
    return NextResponse.json({ error: "Failed to fetch time slots." }, { status: 500 });
  }
}