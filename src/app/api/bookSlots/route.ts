// app/api/timeslots/route.ts
import { NextResponse } from 'next/server';
import axios from 'axios';
import { Ratelimit } from '@upstash/ratelimit'
import { kv } from '@vercel/kv'
export async function POST(request: Request) {
  try {
    if (process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN) {
        const ip = request.headers.get('x-forwarded-for')
        const ratelimit = new Ratelimit({
          redis: kv,
          // rate limit to 1 request per 1 hour
          limiter: Ratelimit.slidingWindow(1, '3600s')
        })
        console.log(ip)
    
        const { success, limit, reset, remaining } = await ratelimit.limit(
          `ratelimit_${ip}`
        )
    
        if (!success) {
          return new Response('You have reached your request limit for the day.', {
            status: 429,
            headers: {
              'X-RateLimit-Limit': limit.toString(),
              'X-RateLimit-Remaining': remaining.toString(),
              'X-RateLimit-Reset': reset.toString()
            }
          })
        }
      } else {
        console.log("KV_REST_API_URL and KV_REST_API_TOKEN env vars not found, not rate limiting...")
      }

    const { slotId, username, email } = await request.json();

    // Send the booking request to your backend API
    const response = await axios.post('https://api.boopr.xyz/bookSlot', {
      slotId,
      username,
      email,
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.BOOPR_API_KEY}`
      },
    });

    if (response.status === 200) {
      return NextResponse.json(response.data);
    } else {
      return NextResponse.json({ error: 'Failed to book the slot' }, { status: response.status });
    }
  } catch (error) {
    console.error('Error booking slot:', error);
    return NextResponse.json({ error: 'An error occurred while booking the slot' }, { status: 500 });
  }
}

export async function GET(request: Request) {
  return NextResponse.json({ error: 'Method not allowed' }, { status: 405 });
}
