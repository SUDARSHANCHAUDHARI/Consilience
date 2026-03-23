import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import App from '../App'

global.fetch = vi.fn()

const mockCouncilResponse = {
  query: 'What is AI?',
  stage1_responses: [
    { model: 'anthropic/claude-opus-4-5', model_name: 'Claude Opus 4.5', response: 'AI is artificial intelligence.' },
    { model: 'openai/gpt-4o', model_name: 'GPT-4o', response: 'AI refers to machine intelligence.' },
  ],
  stage2_reviews: [
    { model: 'anthropic/claude-opus-4-5', model_name: 'Claude Opus 4.5', review: 'Both responses are accurate.' },
  ],
  stage3_final: 'AI, or Artificial Intelligence, is the simulation of human intelligence by machines.',
  timestamp: '2024-01-01T00:00:00',
}

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the header', () => {
    render(<App />)
    expect(screen.getByText('🧠 Consilience')).toBeInTheDocument()
  })

  it('renders the query input and submit button', () => {
    render(<App />)
    expect(screen.getByPlaceholderText('Ask your question...')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Ask Council' })).toBeInTheDocument()
  })

  it('does not submit when query is empty', () => {
    render(<App />)
    fireEvent.click(screen.getByRole('button', { name: 'Ask Council' }))
    expect(global.fetch).not.toHaveBeenCalled()
  })

  it('disables input and button while loading', async () => {
    global.fetch.mockImplementation(() => new Promise(() => {}))
    render(<App />)

    fireEvent.change(screen.getByPlaceholderText('Ask your question...'), {
      target: { value: 'What is AI?' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Ask Council' }))

    expect(screen.getByPlaceholderText('Ask your question...')).toBeDisabled()
    expect(screen.getByRole('button', { name: 'Processing...' })).toBeDisabled()
  })

  it('shows error banner on network failure', async () => {
    global.fetch.mockRejectedValue(new Error('Network error'))
    render(<App />)

    fireEvent.change(screen.getByPlaceholderText('Ask your question...'), {
      target: { value: 'What is AI?' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Ask Council' }))

    await waitFor(() => {
      expect(screen.getByText('Network error')).toBeInTheDocument()
    })
  })

  it('shows error banner when server returns error status', async () => {
    global.fetch.mockResolvedValue({
      ok: false,
      status: 500,
      json: async () => ({ detail: 'Internal server error' }),
    })
    render(<App />)

    fireEvent.change(screen.getByPlaceholderText('Ask your question...'), {
      target: { value: 'What is AI?' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Ask Council' }))

    await waitFor(() => {
      expect(screen.getByText('Internal server error')).toBeInTheDocument()
    })
  })

  it('clears previous error when submitting again', async () => {
    global.fetch.mockRejectedValueOnce(new Error('First error'))
    render(<App />)

    const input = screen.getByPlaceholderText('Ask your question...')
    fireEvent.change(input, { target: { value: 'What is AI?' } })
    fireEvent.click(screen.getByRole('button', { name: 'Ask Council' }))

    await waitFor(() => expect(screen.getByText('First error')).toBeInTheDocument())

    global.fetch.mockImplementation(() => new Promise(() => {}))
    fireEvent.click(screen.getByRole('button', { name: 'Ask Council' }))

    await waitFor(() => expect(screen.queryByText('First error')).not.toBeInTheDocument())
  })

  it('renders stage 1 responses after successful query', async () => {
    global.fetch.mockResolvedValue({ ok: true, json: async () => mockCouncilResponse })
    render(<App />)

    fireEvent.change(screen.getByPlaceholderText('Ask your question...'), {
      target: { value: 'What is AI?' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Ask Council' }))

    await waitFor(() => {
      expect(screen.getByText('📝 Stage 1: Individual Responses')).toBeInTheDocument()
      expect(screen.getByRole('button', { name: 'Claude Opus 4.5' })).toBeInTheDocument()
      expect(screen.getByRole('button', { name: 'GPT-4o' })).toBeInTheDocument()
    })
  })

  it('renders stage 3 final answer after successful query', async () => {
    global.fetch.mockResolvedValue({ ok: true, json: async () => mockCouncilResponse })
    render(<App />)

    fireEvent.change(screen.getByPlaceholderText('Ask your question...'), {
      target: { value: 'What is AI?' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Ask Council' }))

    await waitFor(() => {
      expect(screen.getByText("👑 Stage 3: Chairman's Final Answer")).toBeInTheDocument()
      expect(screen.getByText(mockCouncilResponse.stage3_final)).toBeInTheDocument()
    })
  })

  it('toggles peer reviews visibility', async () => {
    global.fetch.mockResolvedValue({ ok: true, json: async () => mockCouncilResponse })
    render(<App />)

    fireEvent.change(screen.getByPlaceholderText('Ask your question...'), {
      target: { value: 'What is AI?' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Ask Council' }))

    await waitFor(() => screen.getByText('Show Reviews'))

    expect(screen.queryByText('Both responses are accurate.')).not.toBeInTheDocument()
    fireEvent.click(screen.getByText('Show Reviews'))
    expect(screen.getByText('Both responses are accurate.')).toBeInTheDocument()
    fireEvent.click(screen.getByText('Hide Reviews'))
    expect(screen.queryByText('Both responses are accurate.')).not.toBeInTheDocument()
  })
})
