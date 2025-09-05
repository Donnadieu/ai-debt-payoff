// Redux slice for payoff plan management

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { PayoffPlan } from '../types';
import { ApiService } from '../services/api';

interface PlanState {
  currentPlan: PayoffPlan | null;
  loading: boolean;
  error: string | null;
}

const initialState: PlanState = {
  currentPlan: null,
  loading: false,
  error: null,
};

// Async thunks
export const calculatePayoffPlan = createAsyncThunk(
  'plan/calculatePayoffPlan',
  async (planRequest: { debts: any[], extra_payment: number, strategy: string }) => {
    const response = await ApiService.calculatePayoffPlan(planRequest);
    return response;
  }
);

const planSlice = createSlice({
  name: 'plan',
  initialState,
  reducers: {
    clearPlan: (state) => {
      state.currentPlan = null;
      state.error = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(calculatePayoffPlan.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(calculatePayoffPlan.fulfilled, (state, action) => {
        state.loading = false;
        state.currentPlan = action.payload;
      })
      .addCase(calculatePayoffPlan.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to calculate payoff plan';
      });
  },
});

export const { clearPlan, clearError } = planSlice.actions;
export default planSlice.reducer;