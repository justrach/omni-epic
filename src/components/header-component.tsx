"use client"
import { motion } from 'framer-motion';
import { Button } from "@/components/ui/button"
import { IoGameController } from "react-icons/io5";
const animationVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

const icons = [
  { IconComponent: FileTextIcon, label: 'Paper', href: 'https://arxiv.org/abs/2405.15568', target: '_blank' },
  // { IconComponent: XIcon, label: 'arXiv', href: '', target: '_blank' },
  // { IconComponent: VideoIcon, label: 'Video', href: '', target: '_blank' },
  { IconComponent: CodeIcon, label: 'Code (Coming soon)', href: '', target: '_blank' },
  // { IconComponent: DatabaseIcon, label: 'Data', href: '', target: '_blank' },
  { IconComponent: XIcon, label: 'Tweet', href: 'https://twitter.com/jeffclune/status/1795787632435212732', target: '_blank' },
  { IconComponent: IoGameController, label: 'Play it yourself!', href: '#game-interface', target: '_self' },
];

export function HeaderComponent() {
  return (
    <div className="max-w-4xl mx-auto space-y-2">
    <motion.h1
      className="text-6xl sm:text-7xl font-bold leading-tight text-center sm:p-4 p-8" 
      initial="hidden"
      animate="visible"
      variants={animationVariants}
      transition={{ duration: 0.5 }}
    >
      OMNI-EPIC:
    </motion.h1>
    <motion.h2
      className="text-4xl sm:text-5xl font-bold leading-tight text-center sm:p-4 p-8"
      initial="hidden"
      animate="visible"
      variants={animationVariants}
      transition={{ duration: 0.5 }}
    >
      Open-endedness via Models of human Notions of Interestingness with Environments Programmed in Code
    </motion.h2>
    <div className="flex flex-col items-center space-y-4  md:text-3xl text-sm p-8 sm:p-4 ">
      <motion.p
        className="text-lg"
        initial="hidden"
        animate="visible"
        variants={animationVariants}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <a href="https://maxencefaldor.github.io/" target="_blank" rel="noopener noreferrer">Maxence Faldor<sup>1 *</sup>, </a>
        <a href="https://www.jennyzhangzt.com/" target="_blank" rel="noopener noreferrer">Jenny Zhang<sup>2,3 *</sup>, </a>
        <a href="https://scholar.google.fr/citations?user=rZtJlPQAAAAJ&hl=fr" target="_blank" rel="noopener noreferrer">Antoine Cully<sup>1 †</sup>, </a>
        <a href="http://jeffclune.com/" target="_blank" rel="noopener noreferrer">Jeff Clune<sup>2,3,4 †</sup></a>
      </motion.p>
      <motion.p
        className="text-lg"
        initial="hidden"
        animate="visible"
        variants={animationVariants}
        transition={{ duration: 0.5, delay: 0.6 }}
      >
        <sup>1</sup>Imperial College London,&nbsp;
        <sup>2</sup>University of British Columbia,&nbsp;
        <sup>3</sup>Vector Institute,&nbsp;
        <sup>4</sup>Canada CIFAR AI Chair
      </motion.p>
      <motion.p
        className="text-lg"
        initial="hidden"
        animate="visible"
        variants={animationVariants}
        transition={{ duration: 0.5, delay: 0.6 }}
      >
        <sup>*</sup>Co-authors,&nbsp;
        <sup>†</sup>Co-senior authors
      </motion.p>
      <div className="flex flex-wrap justify-center gap-4">
        {icons.map((icon, index) => (
          <motion.div
            key={icon.label}
            initial="hidden"
            animate="visible"
            variants={animationVariants}
            transition={{ duration: 0.5, delay: 0.9 + index * 0.2 }}
          >
            {icon.href ? (
              <a href={icon.href} target={icon.target} rel="noopener noreferrer">
                <Button className="bg-black text-white py-2 px-4 rounded-full inline-flex items-center">
                  <icon.IconComponent className="mr-2" />
                  {icon.label}
                </Button>
              </a>
            ) : (
              <Button className="bg-black text-white py-2 px-4 rounded-full inline-flex items-center">
                <icon.IconComponent className="mr-2" />
                {icon.label}
              </Button>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  </div>
  )
}

function ArchiveXIcon(props:any) {
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
      <rect width="20" height="5" x="2" y="3" rx="1" />
      <path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8" />
      <path d="m9.5 17 5-5" />
      <path d="m9.5 12 5 5" />
    </svg>
  )
}


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


function DatabaseIcon(props:any) {
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
      <ellipse cx="12" cy="5" rx="9" ry="3" />
      <path d="M3 5V19A9 3 0 0 0 21 19V5" />
      <path d="M3 12A9 3 0 0 0 21 12" />
    </svg>
  )
}


function FileTextIcon(props:any) {
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
      <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z" />
      <path d="M14 2v4a2 2 0 0 0 2 2h4" />
      <path d="M10 9H8" />
      <path d="M16 13H8" />
      <path d="M16 17H8" />
    </svg>
  )
}




function VideoIcon(props:any) {
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
      <path d="m16 13 5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5" />
      <rect x="2" y="6" width="14" height="12" rx="2" />
    </svg>
  )
}


function XIcon(props:any) {
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
      <path d="M18 6 6 18" />
      <path d="m6 6 12 12" />
    </svg>
  )
}