// Redux store configuration for the debt payoff mobile app

import { configureStore } from '@reduxjs/toolkit';
import debtSlice from './debtSlice';
import planSlice from './planSlice';

export const store = configureStore({
  reducer: {
    debts: debtSlice,
    plan: planSlice,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;