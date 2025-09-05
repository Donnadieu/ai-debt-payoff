import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { Provider } from 'react-redux';
import { store } from './src/store';
import AppNavigator from './src/navigation/AppNavigator';

import { GluestackUIProvider } from '@/components/ui/gluestack-ui-provider';
import '@/global.css';

export default function App() {
  return (
    <GluestackUIProvider mode="dark">
      <Provider store={store}>
        <AppNavigator />
        <StatusBar style="light" />
      </Provider>
    </GluestackUIProvider>
  );
}
