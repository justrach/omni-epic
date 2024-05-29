import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"


export async function copyTextToClipboard(text: string): Promise<void> {
  if ('clipboard' in navigator) {
    await navigator.clipboard.writeText(text);
  } else {
    document.execCommand('copy', true, text);
  }
}

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
