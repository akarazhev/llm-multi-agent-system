/**
 * PageTitle Component (Molecule)
 * Sets document title and meta tags for pages
 */

import { useEffect } from 'react';

export interface PageTitleProps {
  title: string;
  description?: string;
}

export function PageTitle({ title, description }: PageTitleProps) {
  useEffect(() => {
    const previousTitle = document.title;
    document.title = `${title} | LLM Multi-Agent System`;

    return () => {
      document.title = previousTitle;
    };
  }, [title]);

  useEffect(() => {
    if (description) {
      let metaDescription = document.querySelector('meta[name="description"]');
      
      if (!metaDescription) {
        metaDescription = document.createElement('meta');
        metaDescription.setAttribute('name', 'description');
        document.head.appendChild(metaDescription);
      }
      
      metaDescription.setAttribute('content', description);
    }
  }, [description]);

  return null;
}
