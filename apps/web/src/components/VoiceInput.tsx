import { useState, useEffect } from 'react';
import { Mic, MicOff } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useToast } from '@/hooks/use-toast';
import { cn } from '@/lib/utils';

interface VoiceInputProps {
  onTranscript: (text: string) => void;
  className?: string;
}

export const VoiceInput = ({ onTranscript, className }: VoiceInputProps) => {
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState<any>(null);
  const { toast } = useToast();

  useEffect(() => {
    if (
      !('webkitSpeechRecognition' in window) &&
      !('SpeechRecognition' in window)
    ) {
      toast({
        title: 'Voice input not supported',
        description: "Your browser doesn't support voice input",
        variant: 'destructive',
      });
      return;
    }

    const SpeechRecognitionAPI =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;
    const recognitionInstance = new SpeechRecognitionAPI();

    recognitionInstance.continuous = true;
    recognitionInstance.interimResults = true;
    recognitionInstance.lang = 'en-US';

    recognitionInstance.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map((result) => result[0])
        .map((result) => result.transcript)
        .join('');

      if (event.results[event.results.length - 1].isFinal) {
        onTranscript(transcript);
      }
    };

    recognitionInstance.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setIsListening(false);
      toast({
        title: 'Voice input error',
        description: 'Failed to process voice input',
        variant: 'destructive',
      });
    };

    recognitionInstance.onend = () => {
      setIsListening(false);
    };

    setRecognition(recognitionInstance);

    return () => {
      if (recognitionInstance) {
        recognitionInstance.stop();
      }
    };
  }, [onTranscript, toast]);

  const toggleListening = () => {
    if (!recognition) return;

    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      recognition.start();
      setIsListening(true);
      toast({
        title: 'Listening...',
        description: 'Speak now to add your task',
      });
    }
  };

  return (
    <Button
      onClick={toggleListening}
      variant={isListening ? 'default' : 'outline'}
      size="icon"
      className={cn(
        'relative transition-all duration-300',
        isListening && 'scale-110 shadow-[0_0_20px_rgba(168,85,247,0.4)]',
        className,
      )}
    >
      {isListening ? (
        <>
          <Mic className="h-5 w-5 animate-pulse" />
          <span className="bg-primary absolute inset-0 animate-ping rounded-full opacity-20" />
        </>
      ) : (
        <MicOff className="h-5 w-5" />
      )}
    </Button>
  );
};
