// LatexWrapper.tsx
import React from 'react';

interface LatexWrapperProps {
  content: string;
}

const LatexWrapper: React.FC<LatexWrapperProps> = ({ content }) => {
  const processLatex = (text: string) => {
    const latexCommands = [
      { command: '\\\\textit', className: 'italic' },
      { command: '\\\\emph', className: 'italic' },
      { command: '\\\\textbf', className: 'font-bold' },
      { command: '\\\\cite', className: 'text-blue-600' },
      { command: '\\\\underline', className: 'underline' },
    ];

    let processedText = text;

    latexCommands.forEach(({ command, className }) => {
      const regex = new RegExp(`${command}\\{(.*?)\\}`, 'g');
      processedText = processedText.replace(regex, (match, content) => {
        const cleanedContent = content.replace(/\\\\/g, '');
        return `<span class="${className}">${cleanedContent}</span>`;
      });
    });

    // Process <strong> tags
    processedText = processedText.replace(/<strong>(.*?)<\/strong>/g, '<span class="font-bold">$1</span>');

    return processedText;
  };

  const renderContent = () => {
    const processedContent = processLatex(content);
    return <span dangerouslySetInnerHTML={{ __html: processedContent }} />;
  };

  return <>{renderContent()}</>;
};

export default LatexWrapper;