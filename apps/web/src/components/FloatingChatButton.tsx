import { MessageCircle, X } from 'lucide-react';
import { Button } from './ui/button';
import { useState } from 'react';
import { ChatInterface } from './ChatInterface';

export const FloatingChatButton = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative">
      <Button
        onClick={() => setIsOpen(!isOpen)}
        className="bg-primary hover:bg-primary/90 size-12 rounded-full shadow-lg"
        size="icon"
      >
        {isOpen ? (
          <X className="size-16" />
        ) : (
          <MessageCircle className="size-16" />
        )}
      </Button>

      {isOpen && <ChatInterface onClose={() => setIsOpen(false)} />}
    </div>
  );
};
