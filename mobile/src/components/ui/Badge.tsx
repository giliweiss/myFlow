import React from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { theme } from '../../theme';

export type BadgeVariant =
  | 'default'
  | 'status-upcoming'
  | 'status-completed'
  | 'status-cancelled';

interface BadgeProps {
  label: string;
  variant?: BadgeVariant;
  style?: ViewStyle;
}

export function Badge({ label, variant = 'default', style }: BadgeProps) {
  return (
    <View style={[styles.base, styles[variant], style]}>
      <Text style={styles.text}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  base: {
    paddingHorizontal: theme.spacing.sm,
    paddingVertical: theme.spacing.xs,
    borderRadius: theme.radius.full,
    alignSelf: 'flex-start',
  },

  default: {
    backgroundColor: theme.colors.primaryLight,
  },

  'status-upcoming': {
    backgroundColor: theme.colors.accent,
  },

  'status-completed': {
    backgroundColor: theme.colors.primary,
  },

  'status-cancelled': {
    backgroundColor: theme.colors.secondary,
  },

  text: {
    ...theme.typography.caption,
    color: theme.colors.textPrimary,
    fontSize: 11,
  },
});
