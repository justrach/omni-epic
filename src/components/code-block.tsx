import { CardTitle, CardDescription, CardHeader, CardContent, Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface Citation {
  id: string;
  text: string;
}

interface CodeBlockProps {
  citations: Citation[];
}

export function CodeBlock({ citations }: CodeBlockProps) {
  const handleCopy = (text:any) => {
    navigator.clipboard.writeText(text).then(() => {
      console.log('Text copied to clipboard');
    }).catch((err) => {
      console.error('Could not copy text: ', err);
    });
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Citation</CardTitle>
        {/* <CardDescription>You can copy these citations directly into your papers!</CardDescription> */}
      </CardHeader>
      <CardContent>
        {citations.map((citation) => (
          <div key={citation.id} className="relative mb-4">
            <div className="flex items-center justify-between gap-4 py-2 px-4 rounded-t-lg bg-gray-800 text-gray-200">
              <div className="flex items-center gap-2">
                <CodeIcon className="w-4 h-4" />
                <span>BibTEX</span>
              </div>
              <Button
                className="text-gray-300 hover:text-white"
                size="sm"
                variant="ghost"
                onClick={() => handleCopy(citation.text)}
              >
                <CopyIcon className="w-4 h-4" />
                <span className="sr-only">Copy code</span>
              </Button>
            </div>
            <pre className="p-4 rounded-b-lg bg-gray-800 text-gray-200 overflow-auto">
              <code>{citation.text}</code>
            </pre>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

// ... (CodeIcon and CopyIcon components remain the same)

function CodeIcon(props:any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <polyline points="16 18 22 12 16 6" />
      <polyline points="8 6 2 12 8 18" />
    </svg>
  )
}


function CopyIcon(props:any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect width="14" height="14" x="8" y="8" rx="2" ry="2" />
      <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" />
    </svg>
  )
}
