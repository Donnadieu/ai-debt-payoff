# MUI Theme Configuration

This directory contains the Material-UI theme configuration for the debt payoff application, integrating existing Tailwind design tokens with MUI components.

## Structure

```
src/theme/
├── index.ts          # Main exports
├── theme.ts          # Core theme configuration
├── colors.ts         # Color palette definitions
├── typography.ts     # Typography configuration
├── breakpoints.ts    # Responsive breakpoint definitions
├── spacing.ts        # Spacing system configuration
├── ThemeProvider.tsx # Theme provider wrapper component
└── README.md         # This documentation
```

## Usage

### Basic Setup

The theme is automatically applied when you wrap your app with the `ThemeProvider`:

```tsx
import { ThemeProvider } from '@/theme';

function App() {
  return (
    <ThemeProvider>
      <YourAppContent />
    </ThemeProvider>
  );
}
```

### Using Theme Values in Components

#### Colors

Access theme colors using the `sx` prop or `useTheme` hook:

```tsx
import { Box, useTheme } from '@mui/material';

// Using sx prop
<Box sx={{ color: 'primary.main', backgroundColor: 'background.paper' }}>
  Content
</Box>

// Using useTheme hook
const theme = useTheme();
<Box sx={{ color: theme.palette.primary.main }}>
  Content
</Box>
```

#### Typography

Use predefined typography variants:

```tsx
import { Typography } from '@mui/material';

<Typography variant="h1">Main Heading</Typography>
<Typography variant="body1">Body text</Typography>
<Typography variant="caption">Small caption text</Typography>
```

#### Spacing

Use the spacing system for consistent layout:

```tsx
import { Box } from '@mui/material';

// Using spacing function (multiples of 4px)
<Box sx={{ p: 2, m: 3 }}> // padding: 8px, margin: 12px
  Content
</Box>

// Using specific spacing values
<Box sx={{ padding: 'spacingValues.4' }}> // 16px
  Content
</Box>
```

#### Responsive Breakpoints

Create responsive layouts using theme breakpoints:

```tsx
import { Box, useMediaQuery, useTheme } from '@mui/material';

const theme = useTheme();
const isMobile = useMediaQuery(theme.breakpoints.down('md'));

<Box sx={{
  flexDirection: { xs: 'column', md: 'row' },
  padding: { xs: 2, sm: 3, md: 4 }
}}>
  Responsive content
</Box>
```

## Color Palette

The theme uses the existing Tailwind color palette:

- **Primary**: Blue (`#0284c7`) - Main brand color
- **Secondary**: Red (`#dc2626`) - Accent color  
- **Success**: Green (`#16a34a`) - Success states
- **Warning**: Yellow (`#d97706`) - Warning states
- **Error**: Red (`#dc2626`) - Error states
- **Grey**: Neutral greys for text and backgrounds

## Typography Scale

The typography system includes:

- **Headings**: h1-h6 with appropriate sizes and weights
- **Body**: body1 (16px) and body2 (14px) for content
- **Captions**: Small text for labels and metadata
- **Buttons**: Specific styling for button text

## Component Customizations

The theme includes customizations for:

- **Button**: Rounded corners, focus states, and hover effects
- **TextField**: Consistent border radius and focus styling
- **Card/Paper**: Custom shadows and border radius
- **Form Elements**: Consistent styling across inputs and labels

## Best Practices

1. **Use sx prop for styling**: Provides type safety and theme integration
2. **Leverage theme spacing**: Use the spacing scale instead of hardcoded values
3. **Use semantic colors**: Choose colors based on meaning (primary, error, etc.)
4. **Follow responsive patterns**: Use breakpoint helpers for consistent layouts
5. **Import from index**: Always import from `@/theme` for centralized access

## Examples

### Custom Component with Theme

```tsx
import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { useTheme } from '@mui/material/styles';

export const CustomCard: React.FC<{ title: string; children: React.ReactNode }> = ({
  title,
  children,
}) => {
  const theme = useTheme();
  
  return (
    <Box
      sx={{
        p: 3,
        borderRadius: 2,
        backgroundColor: 'background.paper',
        boxShadow: theme.shadows[2],
        border: `1px solid ${theme.palette.divider}`,
      }}
    >
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      {children}
    </Box>
  );
};
```

### Responsive Grid

```tsx
import { Grid, Container } from '@mui/material';

<Container maxWidth="lg">
  <Grid container spacing={{ xs: 2, md: 3 }}>
    <Grid item xs={12} sm={6} md={4}>
      <CustomCard title="Card 1">Content</CustomCard>
    </Grid>
    <Grid item xs={12} sm={6} md={4}>
      <CustomCard title="Card 2">Content</CustomCard>
    </Grid>
  </Grid>
</Container>
```