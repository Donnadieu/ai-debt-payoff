import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { debtFormInputSchema, debtFormSchema, defaultDebtValues } from '../../schemas/debt';
import type { DebtFormInput, DebtFormData } from '../../schemas/debt';
import { Button } from '../Button/Button';
import { Input } from '../Input/Input';
import { Select } from '../Select/Select';
import { TextArea } from '../TextArea/TextArea';
import { Card } from '../Card/Card';

interface DebtFormProps {
  onSubmit: (data: DebtFormData) => void;
  initialData?: Partial<DebtFormData>;
  isLoading?: boolean;
  submitLabel?: string;
}

export const DebtForm: React.FC<DebtFormProps> = ({
  onSubmit,
  initialData,
  isLoading = false,
  submitLabel = 'Save Debt'
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
    watch
  } = useForm<DebtFormInput>({
    resolver: zodResolver(debtFormInputSchema),
    defaultValues: { ...defaultDebtValues, ...initialData } as DebtFormInput
  });

  const watchedBalance = watch('balance');
  const watchedMinPayment = watch('minimumPayment');

  const onFormSubmit = async (data: DebtFormData) => {
    try {
      await onSubmit(data);
      if (!initialData) {
        reset();
      }
    } catch (error) {
      console.error('Form submission error:', error);
    }
  };

  const debtTypeOptions = [
    { value: 'credit_card', label: 'Credit Card' },
    { value: 'loan', label: 'Personal Loan' },
    { value: 'mortgage', label: 'Mortgage' },
    { value: 'other', label: 'Other' }
  ];

  const statusOptions = [
    { value: 'active', label: 'Active' },
    { value: 'paid_off', label: 'Paid Off' },
    { value: 'closed', label: 'Closed' }
  ];

  return (
    <Card className="p-6">
      <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="md:col-span-2">
            <Input
              label="Debt Name"
              placeholder="e.g., Chase Freedom Credit Card"
              error={errors.name?.message}
              {...register('name')}
            />
          </div>

          <div>
            <Input
              label="Current Balance"
              type="number"
              step="0.01"
              placeholder="0.00"
              error={errors.balance?.message}
              {...register('balance')}
            />
            {watchedBalance && (
              <p className="text-sm text-gray-600 mt-1">
                ${parseFloat(watchedBalance).toLocaleString()}
              </p>
            )}
          </div>

          <div>
            <Input
              label="APR (%)"
              type="number"
              step="0.01"
              placeholder="0.00"
              error={errors.apr?.message}
              {...register('apr')}
            />
          </div>

          <div>
            <Input
              label="Minimum Payment"
              type="number"
              step="0.01"
              placeholder="0.00"
              error={errors.minimumPayment?.message}
              {...register('minimumPayment')}
            />
            {watchedMinPayment && (
              <p className="text-sm text-gray-600 mt-1">
                ${parseFloat(watchedMinPayment).toLocaleString()}
              </p>
            )}
          </div>

          <div>
            <Select
              label="Debt Type"
              options={debtTypeOptions}
              error={errors.type?.message}
              {...register('type')}
            />
          </div>

          <div>
            <Select
              label="Status"
              options={statusOptions}
              error={errors.status?.message}
              {...register('status')}
            />
          </div>

          <div className="md:col-span-2">
            <TextArea
              label="Description (Optional)"
              placeholder="Additional notes about this debt..."
              rows={3}
              error={errors.description?.message}
              {...register('description')}
            />
          </div>
        </div>

        <div className="flex justify-end space-x-3">
          <Button
            type="button"
            variant="outline"
            onClick={() => reset()}
            disabled={isSubmitting || isLoading}
          >
            Reset
          </Button>
          <Button
            type="submit"
            disabled={isSubmitting || isLoading}
            loading={isSubmitting || isLoading}
          >
            {submitLabel}
          </Button>
        </div>
      </form>
    </Card>
  );
};
