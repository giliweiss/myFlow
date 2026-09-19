import { View, StyleSheet, ScrollView } from 'react-native';
import { TextField, Button } from '../ui';
import { theme } from '../../theme';
import { strings } from '../../i18n/he';
import type { InstructorExerciseFormValues } from '../../lib/instructor-exercise-form';

interface InstructorExerciseFormProps {
  values: InstructorExerciseFormValues;
  onChange: (values: InstructorExerciseFormValues) => void;
  onSubmit: () => void;
  submitLabel: string;
  loading?: boolean;
  extraActions?: React.ReactNode;
}

export function InstructorExerciseForm({
  values,
  onChange,
  onSubmit,
  submitLabel,
  loading = false,
  extraActions,
}: InstructorExerciseFormProps) {
  const updateField = <K extends keyof InstructorExerciseFormValues>(
    field: K,
    value: InstructorExerciseFormValues[K],
  ) => {
    onChange({ ...values, [field]: value });
  };

  return (
    <ScrollView
      contentContainerStyle={styles.scrollContent}
      keyboardShouldPersistTaps="handled"
    >
      <View style={styles.container}>
        <TextField
          label={strings.exercises.nameHe}
          placeholder={strings.exercises.nameHe}
          value={values.nameHe}
          onChangeText={(text) => updateField('nameHe', text)}
        />
        <TextField
          label={strings.exercises.nameEn}
          placeholder={strings.exercises.nameEn}
          value={values.nameEn}
          onChangeText={(text) => updateField('nameEn', text)}
        />
        <TextField
          label={strings.exercises.descriptionHe}
          placeholder={strings.exercises.descriptionHe}
          value={values.descriptionHe}
          onChangeText={(text) => updateField('descriptionHe', text)}
          multiline
          numberOfLines={3}
        />
        <TextField
          label={strings.exercises.difficultyLevel}
          placeholder={strings.exercises.difficultyPlaceholder}
          value={values.level}
          onChangeText={(text) => updateField('level', text)}
        />
        <TextField
          label={strings.exercises.bodyFocus}
          placeholder={strings.exercises.bodyFocusPlaceholder}
          value={values.bodyFocus}
          onChangeText={(text) => updateField('bodyFocus', text)}
        />
        <TextField
          label={strings.exercises.equipment}
          placeholder={strings.exercises.equipmentPlaceholder}
          value={values.equipment}
          onChangeText={(text) => updateField('equipment', text)}
        />
        <TextField
          label={strings.exercises.teachingNotes}
          placeholder={strings.exercises.teachingNotes}
          value={values.teachingNotes}
          onChangeText={(text) => updateField('teachingNotes', text)}
          multiline
          numberOfLines={4}
        />

        <Button
          label={submitLabel}
          onPress={onSubmit}
          loading={loading}
          style={styles.submitButton}
        />

        {extraActions}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scrollContent: {
    paddingBottom: theme.spacing.xl,
  },

  container: {
    paddingHorizontal: theme.spacing.md,
    gap: theme.spacing.md,
  },

  submitButton: {
    marginTop: theme.spacing.sm,
  },
});
