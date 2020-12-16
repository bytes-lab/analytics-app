import React from 'react'
import { render, screen } from 'test'
import ErrorMessage from '../error-message'

test('render ErrorMessage', () => {
  // Show ErrorMessage
  const { rerender } = render(<ErrorMessage>Test</ErrorMessage>)
  expect(screen.getByText(/test/i)).toBeInTheDocument()
  // Hide ErrorMessage
  rerender(<ErrorMessage show={false}>Test</ErrorMessage>)
  expect(screen.queryByText(/test/i)).not.toBeInTheDocument()
})
