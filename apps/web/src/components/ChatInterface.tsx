import { useToast } from '@/hooks/use-toast';
import { ChatMessage } from '@/shared/types';
import { useNotifs } from '@/store';
import { Mic, MicOff, Send } from 'lucide-react';
import { useCallback, useRef, useState } from 'react';
import { Button } from './ui/button';
import { ScrollArea } from './ui/scroll-area';
import { Textarea } from './ui/textarea';
import { VoiceInput } from './VoiceInput';

interface ChatInterfaceProps {
  onClose: () => void;
}

export const ChatInterface = ({ onClose }: ChatInterfaceProps) => {
  const chatMessages = useNotifs((state) => state.chatMessages);
  const addChatMessage = useNotifs((state) => state.addChatMessage);

  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const { toast } = useToast();
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);

  const handleSend = useCallback(async () => {
    if (!input.trim()) return;

    addChatMessage({
      id: Date.now().toString(),
      role: 'user',
      content: input,
    });
    setInput('');

    const res = await fetch(import.meta.env.VITE_API_URL + '/chat/message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_message: input }),
    });
    const data = await res.json();

    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'assistant',
      content: data.response,
    };
    addChatMessage(newMessage);
  }, [input]);

  const handleTranscript = (text: string) => {
    setInput(text);
  };

  const toggleRecording = async () => {
    if (!isRecording) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;

        const audioChunks: Blob[] = [];

        mediaRecorder.ondataavailable = (event) => {
          audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
          const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
          // Here you would send the audio to a speech-to-text service
          toast({
            title: 'Voice recorded',
            description: 'Voice input feature coming soon!',
          });
          stream.getTracks().forEach((track) => track.stop());
        };

        mediaRecorder.start();
        setIsRecording(true);
      } catch (error) {
        toast({
          title: 'Error',
          description: 'Could not access microphone',
          variant: 'destructive',
        });
      }
    } else {
      mediaRecorderRef.current?.stop();
      setIsRecording(false);
    }
  };

  return (
    <div className="bg-card border-border absolute bottom-20 left-1/2 z-40 flex h-screen max-h-[calc(100vh-12rem)] w-[calc(100vw-2rem)] max-w-[600px] -translate-x-1/2 flex-col rounded-2xl border shadow-2xl">
      {/* Header */}
      <div className="border-border border-b p-4">
        <h3 className="text-foreground font-semibold">Health Assistant</h3>
        <p className="text-muted-foreground text-xs">
          Ask me anything about your health
        </p>
      </div>

      {/* Messages */}
      <ScrollArea className="flex-1 p-4">
        <div className="space-y-4">
          {chatMessages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-2 ${
                  message.role === 'user'
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted text-foreground'
                }`}
              >
                <p className="text-sm">{message.content}</p>
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>

      {/* Input */}
      <div className="border-border border-t p-4">
        <div className="flex gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder="Type a message..."
            className="h-10 min-h-10 resize-none"
          />
          <div className="flex items-center justify-end gap-2">
            <Button size="icon" onClick={handleSend} disabled={!input.trim()}>
              <Send className="h-4 w-4" />
            </Button>

            <VoiceInput onTranscript={handleTranscript} />
          </div>
        </div>
      </div>
    </div>
  );
};
