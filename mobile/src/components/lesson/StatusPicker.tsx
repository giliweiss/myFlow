import { View, StyleSheet, Pressable } from 'react-native';
import { Badge } from '../ui';
import { theme } from '../../theme';
import { STATUS_LABELS, STATUS_VARIANTS } from '../../lib/lesson-status';
import type { LessonStatus } from '../../types/lesson';

interface StatusPickerProps {
  value: LessonStatus;
  options: LessonStatus[];
  onChange: (status: LessonStatus) => void;
  disabled?: boolean;
}

export function StatusPicker({
  value,
  options,
  onChange,
  disabled = false,
}: StatusPickerProps) {
  return (
    <View style={styles.container}>
      {options.map((status) => {
        const isSelected = status === value;

        return (
          <Pressable
            key={status}
            disabled={disabled}
            onPress={() => onChange(status)}
            style={({ pressed }) => [
              styles.option,
              isSelected && styles.optionSelected,
              pressed && !disabled && styles.optionPressed,
              disabled && styles.optionDisabled,
            ]}
          >
            <Badge
              label={STATUS_LABELS[status]}
              variant={STATUS_VARIANTS[status]}
            />
          </Pressable>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row-reverse',
    flexWrap: 'wrap',
    gap: theme.spacing.sm,
  },

  option: {
    borderRadius: theme.radius.full,
    padding: 2,
  },

  optionSelected: {
    borderWidth: 2,
    borderColor: theme.colors.primary,
  },

  optionPressed: {
    opacity: 0.85,
  },

  optionDisabled: {
    opacity: 0.6,
  },
});
