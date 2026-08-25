import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import * as Icons from 'lucide-react-native';
import { theme } from '../../theme';
import { Button } from './Button';

interface EmptyStateProps {
  title: string;
  message: string;
  iconName?: keyof typeof Icons;
  actionLabel?: string;
  onAction?: () => void;
}

export function EmptyState({
  title,
  message,
  iconName = 'Inbox',
  actionLabel,
  onAction,
}: EmptyStateProps) {
  const IconComponent = (Icons as any)[iconName];

  return (
    <View style={styles.container}>
      {IconComponent && (
        <IconComponent
          size={48}
          color={theme.colors.textSecondary}
          strokeWidth={1.5}
          style={styles.icon}
        />
      )}
      <Text style={[theme.typography.title, styles.title]}>{title}</Text>
      <Text style={[theme.typography.body, styles.message]}>{message}</Text>
      {actionLabel && onAction && (
        <Button
          label={actionLabel}
          onPress={onAction}
          variant="primary"
          style={styles.button}
        />
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

  icon: {
    marginBottom: theme.spacing.lg,
  },

  title: {
    marginBottom: theme.spacing.sm,
    textAlign: 'center',
  },

  message: {
    marginBottom: theme.spacing.lg,
    textAlign: 'center',
    color: theme.colors.textSecondary,
  },

  button: {
    minWidth: 150,
  },
});
