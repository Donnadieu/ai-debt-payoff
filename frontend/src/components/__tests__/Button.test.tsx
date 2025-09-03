import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { ThemeProvider } from '@mui/material/styles';
import { Button } from '../Button/Button';
import { theme } from '../../theme';

// Helper function to render with theme
const renderWithTheme = (component: React.ReactElement) => {
  return render(<ThemeProvider theme={theme}>{component}</ThemeProvider>);
};

describe('Button', () => {
  it('renders with default props', () => {
    renderWithTheme(<Button>Click me</Button>);
    const button = screen.getByRole('button', { name: /click me/i });
    expect(button).toBeInTheDocument();
    expect(button).toHaveClass('MuiButton-root');
    expect(button).toHaveClass('MuiButton-contained');
  });

  it('renders different variants correctly', () => {
    const { rerender } = renderWithTheme(<Button variant='secondary'>Secondary</Button>);
    expect(screen.getByRole('button')).toHaveClass('MuiButton-containedSecondary');

    rerender(<Button variant='danger'>Danger</Button>);
    expect(screen.getByRole('button')).toHaveClass('MuiButton-containedError');

    rerender(<Button variant='outline'>Outline</Button>);
    expect(screen.getByRole('button')).toHaveClass('MuiButton-outlined');
  });

  it('renders different sizes correctly', () => {
    const { rerender } = renderWithTheme(<Button size='sm'>Small</Button>);
    expect(screen.getByRole('button')).toHaveClass('MuiButton-sizeSmall');

    rerender(<Button size='lg'>Large</Button>);
    expect(screen.getByRole('button')).toHaveClass('MuiButton-sizeLarge');
  });

  it('handles loading state', () => {
    renderWithTheme(<Button loading>Loading</Button>);
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
    expect(screen.getByText('Loading...')).toBeInTheDocument();
    // Check for loading spinner
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('handles disabled state', () => {
    renderWithTheme(<Button disabled>Disabled</Button>);
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
    expect(button).toHaveClass('Mui-disabled');
  });

  it('handles click events', () => {
    const handleClick = jest.fn();
    renderWithTheme(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('renders with full width', () => {
    renderWithTheme(<Button fullWidth>Full Width</Button>);
    expect(screen.getByRole('button')).toHaveClass('MuiButton-fullWidth');
  });

  it('renders with icons', () => {
    const startIcon = <span data-testid='start-icon'>→</span>;
    const endIcon = <span data-testid='end-icon'>←</span>;

    renderWithTheme(
      <Button startIcon={startIcon} endIcon={endIcon}>
        With Icons
      </Button>
    );

    expect(screen.getByTestId('start-icon')).toBeInTheDocument();
    expect(screen.getByTestId('end-icon')).toBeInTheDocument();
  });
});
