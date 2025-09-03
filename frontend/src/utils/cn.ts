/**
 * Utility function to combine and filter class names
 * Similar to clsx or classnames but simplified for our needs
 */
export const cn = (...classes: (string | undefined | null | boolean)[]): string => {
  return classes
    .filter(Boolean)
    .join(' ')
    .trim();
};

export default cn;