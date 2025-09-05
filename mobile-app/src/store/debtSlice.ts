// Redux slice for debt management

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Debt } from '../types';
import { ApiService } from '../services/api';

interface DebtState {
  debts: Debt[];
  loading: boolean;
  error: string | null;
}

const initialState: DebtState = {
  debts: [],
  loading: false,
  error: null,
};

// Async thunks
export const fetchDebts = createAsyncThunk(
  'debts/fetchDebts',
  async () => {
    const response = await ApiService.getDebts();
    return response.debts || [];
  }
);

export const createDebt = createAsyncThunk(
  'debts/createDebt',
  async (debtData: Omit<Debt, 'id' | 'created_at' | 'updated_at'>) => {
    const response = await ApiService.createDebt(debtData);
    return response.debt;
  }
);

const debtSlice = createSlice({
  name: 'debts',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch debts
      .addCase(fetchDebts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDebts.fulfilled, (state, action) => {
        state.loading = false;
        state.debts = action.payload;
      })
      .addCase(fetchDebts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch debts';
      })
      // Create debt
      .addCase(createDebt.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createDebt.fulfilled, (state, action) => {
        state.loading = false;
        if (action.payload) {
          state.debts.push(action.payload);
        }
      })
      .addCase(createDebt.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to create debt';
      });
  },
});

export const { clearError } = debtSlice.actions;
export default debtSlice.reducer;