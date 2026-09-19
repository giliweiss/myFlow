import React from 'react';
import { View, ActivityIndicator, Text, StyleSheet } from 'react-native';
import { theme } from '../../theme';

interface LoadingStateProps {
  message?: string;
  subtitle?: string;
}

export function LoadingState({ message = 'טוען...', subtitle }: LoadingStateProps) {
  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color={theme.colors.primary} />
      {message ? (
        <Text style={[theme.typography.body, styles.message]}>{message}</Text>
      ) : null}
      {subtitle ? (
        <Text style={[theme.typography.caption, styles.subtitle]}>{subtitle}</Text>
      ) : null}
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

  subtitle: {
    marginTop: theme.spacing.sm,
    textAlign: 'center',
    color: theme.colors.textSecondary,
  },
});
