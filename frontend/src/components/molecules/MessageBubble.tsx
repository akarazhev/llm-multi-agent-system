/**
 * MessageBubble Component (Molecule)
 * Chat message bubble with agent/system styling
 * Based on OPERATIONAL_DASHBOARD_RESEARCH.md Phase 3.2
 */

import { cn } from '@utils/cn';
import { User, Bot, AlertCircle, CheckCircle2 } from 'lucide-react';

export type MessageType = 'agent' | 'system' | 'error' | 'success';

export interface ChatMessage {
  id: string;
  type: MessageType;
  content: string;
  sender?: string;
  timestamp: string;
  avatar?: string;
}

export interface MessageBubbleProps {
  message: ChatMessage;
  className?: string;
}

const messageStyles: Record<MessageType, {
  bgColor: string;
  textColor: string;
  icon: React.ReactNode;
  align: 'left' | 'right';
}> = {
  agent: {
    bgColor: 'bg-primary/10 dark:bg-primary/20',
    textColor: 'text-text-primary',
    icon: <Bot className="h-5 w-5" />,
    align: 'left',
  },
  system: {
    bgColor: 'bg-background-secondary',
    textColor: 'text-text-secondary',
    icon: <User className="h-5 w-5" />,
    align: 'right',
  },
  error: {
    bgColor: 'bg-red-50 dark:bg-red-900/20',
    textColor: 'text-red-600',
    icon: <AlertCircle className="h-5 w-5" />,
    align: 'left',
  },
  success: {
    bgColor: 'bg-green-50 dark:bg-green-900/20',
    textColor: 'text-green-600',
    icon: <CheckCircle2 className="h-5 w-5" />,
    align: 'left',
  },
};

export function MessageBubble({ message, className }: MessageBubbleProps) {
  const style = messageStyles[message.type];
  const isRight = style.align === 'right';

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={cn(
      'flex gap-3 mb-4',
      isRight ? 'flex-row-reverse' : 'flex-row',
      className
    )}>
      {/* Avatar */}
      <div className={cn(
        'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
        message.type === 'agent' && 'bg-primary text-white',
        message.type === 'system' && 'bg-gray-500 text-white',
        message.type === 'error' && 'bg-red-500 text-white',
        message.type === 'success' && 'bg-green-500 text-white',
      )}>
        {message.avatar ? (
          <img 
            src={message.avatar} 
            alt={message.sender || 'Avatar'} 
            className="w-full h-full rounded-full object-cover"
          />
        ) : (
          style.icon
        )}
      </div>

      {/* Message Content */}
      <div className={cn(
        'max-w-[70%] flex flex-col',
        isRight ? 'items-end' : 'items-start'
      )}>
        {/* Sender Name */}
        {message.sender && (
          <span className="text-xs text-text-tertiary mb-1">
            {message.sender}
          </span>
        )}

        {/* Bubble */}
        <div className={cn(
          'px-4 py-3 rounded-2xl',
          style.bgColor,
          style.textColor,
          isRight ? 'rounded-tr-md' : 'rounded-tl-md'
        )}>
          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        </div>

        {/* Timestamp */}
        <span className="text-xs text-text-tertiary mt-1">
          {formatTime(message.timestamp)}
        </span>
      </div>
    </div>
  );
}
