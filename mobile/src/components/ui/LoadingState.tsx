import React from 'react';
import { View, ActivityIndicator, Text, StyleSheet } from 'react-native';
import { theme } from '../../theme';

interface LoadingStateProps {
  message?: string;
}

export function LoadingState({ message = 'טוען...' }: LoadingStateProps) {
  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color={theme.colors.primary} />
      {message && (
        <Text style={[theme.typography.body, styles.message]}>{message}</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: theme.spacing.md,
  },

  message: {
    marginTop: theme.spacing.md,
    textAlign: 'center',
  },
});
