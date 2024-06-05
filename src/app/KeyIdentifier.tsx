"use client"
import { Connected } from '@/components/ui/connected/connected';
import { NotConnected } from '@/components/ui/connected/notconnected';
import React, { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import { Button } from "@/components/ui/button"
import { ToastAction } from "@/components/ui/toast"
import { useToast } from "@/components/ui/use-toast"
import { ToastDemo } from '@/components/ui/connected/toast';
import { AccessGranted, EnvDescriptionEvent } from '../../types/socket_types';
import { ResetAlertDialog } from '@/components/ui/next_level/button_level';
import Link from 'next/link';
export function SocketIdentifier() {
  const { toast } = useToast()
  const [connected, setConnected] = useState(false);
  const [levelFinished, setLevelFinishedToast] = useState(false); // State to track if the next level toast has been shown
  const [newSocket, setSocket] = useState<Socket | null>(null);
  const [accessCode, setAccessCode] = useState('');
  const [accessGranted, setAccessGranted] = useState(false);
  const [showAccessCode, setShowAccessCode] = useState(false);
  const [currAccessCode, setCurrAccessCode] = useState('');
  const [nextLevelLoading, setNextLevelLoading] = useState(false);

  useEffect(() => {
    // This side effect reacts to the change in level completion status.
    if (levelFinished) {
      // Show the toast for level completion.
      toast({
        title: "Level Completed",
        duration: 6000,
        description: 'Prepare for new challenges!',
        action: (
          <ToastAction altText="Dismiss">Dismiss</ToastAction>
        ),
      });
    }
  }, [levelFinished, toast]);
  useEffect(() => {

    const socket = io(process.env.NEXT_PUBLIC_API_URL!,{
      transports: ['websocket', 'polling']
    });
    setSocket(socket);

    socket.on('connect', () => {
      console.log('Connected to Socket.IO server');
      setConnected(true);
    });
    socket.on('disconnect', () => {
      console.log('Disconnected from Socket.IO server');
      setConnected(false);
    });

    socket.on('env_description', (data: EnvDescriptionEvent) => {
      toast({
        className: 'text-4xl ',
        title: 'Instructions for the current level:',
        description: <div>{data.description.split('\n').map(
          (line, index) => (
            <div key={index}>{line}<br/></div>
          )
        )}</div>,
        duration: 30000,
        action: (
          <ToastAction altText="View details" >Close</ToastAction>
        ),
      });
    });

    socket.on('reset_message', ()=>{
      setLevelFinishedToast(false);
    })

    socket.on('level_complete', () => {
      setLevelFinishedToast(true);
    });

    socket.on('next_level', () => {
      setLevelFinishedToast(false);
    });

    socket.on('access_granted', (data: AccessGranted) => {
      if(data.granted===true){
        toast({
          className: 'text-4xl ',
          title: 'You are now controlling the robot!',
          description: <div>Happy playing :-&#41;</div>,
          duration: 3000,
          action: (
            <ToastAction altText="View details" >Close</ToastAction>
          ),
        });
      }
      else{
        toast({
          className: 'text-4xl ',
          title: 'Please get a timeslot at the waitlist:',
          description: <div><Link href="/waitlist" className="text-purple-500 underline">Click me!</Link></div>,
          duration: 3000,
          action: (
            <ToastAction altText="View details" >Close</ToastAction>
          ),
        });
      }
    });

    socket.on('show_access_code', (data: { show: boolean; accessCode: string }) => {
      setShowAccessCode(data.show);
      if (data.show) {
        setCurrAccessCode(data.accessCode);
      }
    });

    socket.on('success_marked', () => {
      toast({
        className: 'text-4xl ',
        title: 'Level marked as success.',
        description: <div>Go to the next level!</div>,
        duration: 3000,
        action: (
          <ToastAction altText="View details" >Close</ToastAction>
        ),
      });
    });

    socket.on('failure_marked', () => {
      toast({
        className: 'text-4xl ',
        title: 'Level marked as failed.',
        description: <div>Go to the next level!</div>,
        duration: 3000,
        action: (
          <ToastAction altText="View details" >Close</ToastAction>
        ),
      });
    });

    socket.on('generating_next_level', (data: { generating: boolean }) => {
      setNextLevelLoading(data.generating);
    });

    const handleKeyDown = (event: KeyboardEvent) => {
      let action;
      switch (event.key) {
        case 'w':
        case 'ArrowUp':
          action = 1; // Go forward
          break;

        case 's':
        case 'ArrowDown':
          action = 2; // Go backward
          break;

        case 'a':
        case 'ArrowLeft':
          action = 4; // Rotate counterclockwise
          break;

        case 'd':
        case 'ArrowRight':
          action = 3; // Rotate clockwise
          break;

        case 'm':
        case 'Spacebar':
          action = 5; // Jump
          break;

        default:
          return;
      }
      if (connected && action !== undefined) {
        socket.emit('action', { action });
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
      socket.off('connect');
      socket.off('disconnect');
      socket.off('level_complete');
      socket.off('next_level');
      socket.off('reset_message');
      socket.off('access_granted');
      socket.off('show_access_code');
      socket.off('success_marked');
      socket.off('failure_marked');
      socket.off('env_description'); // Clean up the listener
      socket.close();
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [connected, toast]); // Include 'toast' in the dependency array to ensure it's captured by useEffect

  const handleAccess = () => {
    newSocket?.emit('access_code', accessCode);
  };

  const handleNextLevel = () => {
    newSocket?.emit('next_level');
    newSocket?.emit('reset');
  };
  const handleReset = () => {
    newSocket?.emit('reset');
  };
  const markSuccess = () => {
    newSocket?.emit('mark_success');
  };
  const markFailure = () => {
    newSocket?.emit('mark_failure');
  };

  return (
    <div className="flex flex-col md:flex-row">
      <div className="flex-shrink-0 mb-8 md:mr-8 max-w-xs overflow-hidden">
        <img src="/images/game_controls.png" alt="Game Controls" className="w-full h-auto object-contain" />
      </div>
      <div className="flex flex-grow flex-col items-center space-y-2">
        {/* <ToastDemo></ToastDemo> */}
        <div className="min-w-full">
          {connected ? <Connected></Connected> : <NotConnected></NotConnected>}
        </div>
        <Button
          onClick={handleNextLevel}
          className="w-full"
          disabled={nextLevelLoading}
        >
          {nextLevelLoading ? (
            <div className="flex items-center justify-center">
              <span className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-purple-500 mr-2"></span>
              <span>Generating next level...</span>
            </div>
          ) : (
            'Next Level'
          )}
        </Button>
        <div className="min-w-full">
          <ResetAlertDialog onConfirm={handleReset}></ResetAlertDialog>
        </div>
        <br/>
        <Button onClick={markSuccess} className="w-full bg-green-300 hover:bg-green-600 text-green-900 hover:text-white">Mark Success</Button>
        <Button onClick={markFailure} className="w-full bg-red-300 hover:bg-red-600 text-red-900 hover:text-white">Mark Failure</Button>
      </div>
      <div className="flex-shrink-0 mb-8 md:ml-8 md:w-64">
        <div className="space-y-2">
          <input
            type="text"
            placeholder="Enter access code"
            value={accessCode}
            onChange={(e) => setAccessCode(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2"
          />
          <Button onClick={handleAccess} className="w-full bg-purple-600 hover:bg-purple-400 text-white">
            Gain Access
          </Button>
          {showAccessCode && (
            <div className="text-center">
              <p>Since no one is controlling the robot now, use this access code:</p>
              <p className="text-lg font-bold">{currAccessCode}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}