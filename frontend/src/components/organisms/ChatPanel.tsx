/**
 * ChatPanel Component (Organism)
 * Scrollable chat panel with messages
 * Based on OPERATIONAL_DASHBOARD_RESEARCH.md Phase 3.1
 */

import { useRef, useEffect, useState } from 'react';
import { cn } from '@utils/cn';
import { MessageBubble, type ChatMessage, type MessageType } from '@components/molecules/MessageBubble';
import { Button, Input, Badge } from '@components/atoms';
import { EmptyState } from '@components/molecules';
import { 
  MessageSquare, 
  Send, 
  Loader2, 
  Filter,
  X,
  ChevronDown
} from 'lucide-react';

export interface ChatPanelProps {
  messages: ChatMessage[];
  isLoading?: boolean;
  onSendMessage?: (message: string) => void;
  height?: number;
  showFilters?: boolean;
  className?: string;
}

const messageTypeFilters: { value: MessageType | 'all'; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'agent', label: 'Agent' },
  { value: 'system', label: 'System' },
  { value: 'error', label: 'Errors' },
  { value: 'success', label: 'Success' },
];

export function ChatPanel({
  messages,
  isLoading,
  onSendMessage,
  height = 500,
  showFilters = true,
  className,
}: ChatPanelProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [inputValue, setInputValue] = useState('');
  const [typeFilter, setTypeFilter] = useState<MessageType | 'all'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [showFilterPanel, setShowFilterPanel] = useState(false);
  const [isAtBottom, setIsAtBottom] = useState(true);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isAtBottom) {
      scrollToBottom();
    }
  }, [messages, isAtBottom]);

  // Track scroll position
  const handleScroll = () => {
    if (!containerRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = containerRef.current;
    setIsAtBottom(scrollHeight - scrollTop - clientHeight < 50);
  };

  // Filter messages
  const filteredMessages = messages.filter((msg) => {
    if (typeFilter !== 'all' && msg.type !== typeFilter) return false;
    if (searchQuery && !msg.content.toLowerCase().includes(searchQuery.toLowerCase())) return false;
    return true;
  });

  const handleSend = () => {
    if (inputValue.trim() && onSendMessage) {
      onSendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const clearFilters = () => {
    setTypeFilter('all');
    setSearchQuery('');
  };

  const hasActiveFilters = typeFilter !== 'all' || searchQuery;

  return (
    <div className={cn('flex flex-col rounded-2xl border border-border bg-background', className)}>
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-border">
        <div className="flex items-center gap-2">
          <MessageSquare className="h-5 w-5 text-primary" />
          <h3 className="font-semibold">Messages</h3>
          <Badge variant="secondary" size="sm">
            {messages.length}
          </Badge>
        </div>
        
        {showFilters && (
          <Button
            size="sm"
            variant={showFilterPanel ? 'secondary' : 'ghost'}
            onClick={() => setShowFilterPanel(!showFilterPanel)}
          >
            <Filter className="h-4 w-4" />
            {hasActiveFilters && (
              <span className="ml-1 w-2 h-2 rounded-full bg-primary" />
            )}
          </Button>
        )}
      </div>

      {/* Filter Panel */}
      {showFilterPanel && (
        <div className="px-4 py-3 border-b border-border bg-background-secondary space-y-3">
          {/* Search */}
          <div className="relative">
            <Input
              type="text"
              placeholder="Search messages..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pr-8"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-text-tertiary hover:text-text-primary"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>

          {/* Type Filters */}
          <div className="flex flex-wrap gap-2">
            {messageTypeFilters.map((filter) => (
              <button
                key={filter.value}
                onClick={() => setTypeFilter(filter.value)}
                className={cn(
                  'px-3 py-1 text-xs rounded-full transition-colors',
                  typeFilter === filter.value
                    ? 'bg-primary text-white'
                    : 'bg-background border border-border hover:bg-background-tertiary'
                )}
              >
                {filter.label}
              </button>
            ))}
            {hasActiveFilters && (
              <button
                onClick={clearFilters}
                className="px-3 py-1 text-xs text-text-secondary hover:text-text-primary"
              >
                Clear
              </button>
            )}
          </div>
        </div>
      )}

      {/* Messages Container */}
      <div
        ref={containerRef}
        onScroll={handleScroll}
        className="flex-1 overflow-y-auto p-4"
        style={{ height: `${height}px` }}
      >
        {isLoading ? (
          <div className="flex items-center justify-center h-full">
            <Loader2 className="h-8 w-8 animate-spin text-text-tertiary" />
          </div>
        ) : filteredMessages.length === 0 ? (
          <EmptyState
            icon={<MessageSquare className="h-12 w-12" />}
            title={hasActiveFilters ? 'No messages match filters' : 'No messages yet'}
            description={hasActiveFilters ? 'Try adjusting your filters' : 'Messages will appear here'}
            action={hasActiveFilters ? { label: 'Clear Filters', onClick: clearFilters, variant: 'outline' } : undefined}
          />
        ) : (
          <>
            {filteredMessages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Scroll to Bottom Button */}
      {!isAtBottom && messages.length > 0 && (
        <button
          onClick={scrollToBottom}
          className="absolute bottom-20 right-4 p-2 rounded-full bg-primary text-white shadow-lg hover:bg-primary-dark transition-colors"
        >
          <ChevronDown className="h-5 w-5" />
        </button>
      )}

      {/* Input */}
      {onSendMessage && (
        <div className="px-4 py-3 border-t border-border">
          <div className="flex items-center gap-2">
            <Input
              type="text"
              placeholder="Type a message..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              className="flex-1"
            />
            <Button
              variant="primary"
              size="sm"
              onClick={handleSend}
              disabled={!inputValue.trim()}
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
