"use client"
import LatexWrapper from '@/app/components/LatexWrapper';
import React, { useState, useEffect } from 'react';
import { CodeBlock } from '../code-block';
import { Label } from '../ui/label';
import { Input } from '../ui/input';
import { Card, CardContent } from "@/components/ui/card"
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"
import Loading from '../loading';



// Interfaces for the academic content
interface AcademicContent {
    abstract: string;
    sections: Section[];
  }
  
  interface Section {
    title: string;
    content: string;
    image?: {
      alt: string;
      src: string;
    };
    video?: {
      alt: string;
      src: string;
    };
    html?: {
      alt: string;
      src: string;
      height?: string;
    };
    html_content?: string;
    longRunTask?: boolean;
    itemData?: { item: number; videoUrl: string; code: string }[];
  }

  interface Citation {
  id: string;
  text: string;
}

interface AcademicContentWithCitations extends AcademicContent {
  citations: Citation[];
}
  
export function AcademicPage() {
  const [data, setData] = useState<AcademicContentWithCitations | null>(null);

  useEffect(() => {
    // Fetching the data from a local JSON file
    fetch('research-paper-content.json')
      .then(response => response.json())
      .then(async (jsonData) => {
        const sectionsWithHtml = await Promise.all(
          jsonData.sections.map(async (section: Section) => {
            if (section.html) {
              const response = await fetch(section.html.src);
              const html_content = await response.text();
              return { ...section, html_content };
            }
            if (section.longRunTask) {
              const itemData = await Promise.all(
                [60, 84, 90, 103, 122, 197].map(async (item) => {
                  try {
                    const videoUrl = `https://documents.paperstowebsite.com/task_${item}.mp4`;
                    const response = await fetch(`/env_codes/long_run/task_${item}.py`);
                    const code = await response.text();
                    return { item, videoUrl, code };
                  } catch (error) {
                    console.error(`Error fetching data for item ${item}:`, error);
                    return { item, videoUrl: null, code: `Error loading code for item ${item}` };
                  }
                })
              );
              return { ...section, itemData };
            }
            return section;
          })
        );
        setData({ ...jsonData, sections: sectionsWithHtml });
      })
      .catch(console.error); // Handle errors appropriately in real applications
  }, []);

  if (!data) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Loading />
      </div>
    ); }

  return (
    <>
      <section className="container py-12 md:py-12">
        <div className="max-w-3xl mx-auto space-y-8">
          <div>
            <h2 className="text-2xl font-bold mb-4">Abstract</h2>
            <p className="text-gray-900 dark:text-gray-400 leading-relaxed">
              <LatexWrapper content={data.abstract} />
            </p>
            </div>
          {data.sections.map((section, index) => (
            <div key={index}>
              <h2 className="text-2xl font-bold mb-4">{section.title}</h2>
              <p className="text-gray-900 dark:text-gray-400 leading-relaxed">
              <LatexWrapper content={section.content} />    
              </p>
              {section.image && (
                <div className="mt-4">
                  <img
                    alt={section.image.alt}
                    className="rounded-lg"
                    style={{
                      width: "100%",
                      height: "auto",
                      objectFit: "cover",
                    }}
                    src={section.image.src}
                    width={800}
                    height={450}
                  />
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                    {section.image.alt}
                  </p>
                </div>
              )}
              {section.video && (
                <div className="mt-4">
                  <video
                    className="rounded-lg"
                    style={{
                      width: "100%",
                      height: "auto",
                      objectFit: "cover",
                    }}
                    src={section.video.src}
                    controls
                  />
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                    {section.video.alt}
                  </p>
                </div>
              )}
              {section.html && (
                <div className="mt-4">
                  <iframe
                    srcDoc={`${section.html_content}`}
                    width="100%"
                    height={section.html.height ? `${section.html.height}` : undefined}
                    style={{ border: 'none' }}
                  ></iframe>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                    {section.html.alt}
                  </p>
                </div>
              )}
              {section.longRunTask && section.itemData && (
                <div className="mt-4">
                  <Carousel className="w-full">
                    <CarouselContent>
                      {section.itemData.map(({ item, videoUrl, code }) => (
                        <CarouselItem key={item}>
                          <div className="p-1 flex w-full max-h-64">
                            <Card className="flex flex-1 flex-col md:flex-row w-full">
                              <div className="flex flex-col md:flex-row w-full">
                                <CardContent className="flex flex-col items-center justify-center p-6 md:w-1/2">
                                  {videoUrl ? (
                                    <>
                                      <span className="text-lg font-semibold mb-2">Task {item}</span>
                                      <video autoPlay muted loop className="w-full">
                                        <source src={videoUrl} type="video/mp4" />
                                        Your browser does not support the video tag.
                                      </video>
                                    </>
                                  ) : (
                                    <span className="text-red-500">Video not available</span>
                                  )}
                                </CardContent>
                                <div className="flex-1 p-4 rounded-b-lg bg-gray-800 text-gray-200 overflow-auto md:w-1/2">
                                  <pre className="text-xs overflow-auto">
                                    <code className="language-python">{code}</code>
                                  </pre>
                                </div>
                              </div>
                            </Card>
                          </div>
                        </CarouselItem>
                      ))}
                    </CarouselContent>
                    <CarouselPrevious />
                    <CarouselNext />
                  </Carousel>
                </div>
              )}
            </div>
          ))}
           <CodeBlock citations={data.citations} />
          <div className="max-w-3xl mx-auto space-y-8">
                <p className="text-gray-900 dark:text-gray-400 leading-relaxed">
              The website template was made by <a href="https://www.rach.codes/" className='text-blue-400'>Rach Pradhan</a> and <a href="https://www.jennyzhangzt.com/" className='text-blue-400'>Jenny Zhang</a>.
              In order to use the template please check it out at <a href="https://github.com/justrach/omni-epic" className='text-blue-400'>this github link</a> and give credit to the original author(s).
            </p>
          </div>
        </div>
      </section>
    </>
  );
}
