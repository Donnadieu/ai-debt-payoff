import { z } from 'zod';

export const debtSchema = z.object({
  id: z.string().optional(),
  
  name: z.string()
    .min(1, 'Debt name is required')
    .max(100, 'Debt name must be less than 100 characters'),
  
  balance: z.number()
    .positive('Balance must be greater than 0')
    .max(999999999, 'Balance must be less than $999,999,999'),
  
  apr: z.number()
    .min(0, 'APR cannot be negative')
    .max(100, 'APR cannot exceed 100%'),
  
  minimumPayment: z.number()
    .positive('Minimum payment must be greater than 0')
    .max(999999, 'Minimum payment must be less than $999,999'),
  
  type: z.enum(['credit_card', 'loan', 'mortgage', 'other'])
    .optional()
    .default('other'),
  
  status: z.enum(['active', 'paid_off', 'closed'])
    .optional()
    .default('active'),
  
  description: z.string()
    .max(500, 'Description must be less than 500 characters')
    .optional(),
    
  createdAt: z.string().optional(),
  updatedAt: z.string().optional(),
});

export const debtFormSchema = debtSchema.extend({
  balance: z.string()
    .min(1, 'Balance is required')
    .transform((val) => parseFloat(val))
    .refine((val) => !isNaN(val) && val > 0, 'Balance must be a valid positive number'),
  
  apr: z.string()
    .min(1, 'APR is required')
    .transform((val) => parseFloat(val))
    .refine((val) => !isNaN(val) && val >= 0 && val <= 100, 'APR must be between 0 and 100'),
  
  minimumPayment: z.string()
    .min(1, 'Minimum payment is required')
    .transform((val) => parseFloat(val))
    .refine((val) => !isNaN(val) && val > 0, 'Minimum payment must be a valid positive number'),
});

export type Debt = z.infer<typeof debtSchema>;
export type DebtFormData = z.infer<typeof debtFormSchema>;

export const defaultDebtValues = {
  name: '',
  balance: '0',
  apr: '0',
  minimumPayment: '0',
  type: 'other' as const,
  status: 'active' as const,
  description: '',
};
