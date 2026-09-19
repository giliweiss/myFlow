import { useEffect, useState } from 'react';
import { Alert, View, StyleSheet } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { ScreenContainer, LoadingState, Button } from '../../../src/components/ui';
import { InstructorExerciseForm } from '../../../src/components/exercise/InstructorExerciseForm';
import { strings } from '../../../src/i18n/he';
import {
  useArchiveInstructorExercise,
  useInstructorExercise,
  useUpdateInstructorExercise,
} from '../../../src/hooks/use-instructor-exercises';
import {
  formValuesToUpdateInput,
  instructorExerciseToFormValues,
  type InstructorExerciseFormValues,
} from '../../../src/lib/instructor-exercise-form';
import { theme } from '../../../src/theme';

export default function EditInstructorExerciseScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const { data: exercise, isLoading, isError } = useInstructorExercise(id ?? '');
  const updateMutation = useUpdateInstructorExercise(id ?? '');
  const archiveMutation = useArchiveInstructorExercise();
  const [values, setValues] = useState<InstructorExerciseFormValues | null>(null);

  useEffect(() => {
    if (exercise) {
      setValues(instructorExerciseToFormValues(exercise));
    }
  }, [exercise]);

  const handleSave = async () => {
    if (!values) {
      return;
    }

    if (!values.nameHe.trim()) {
      Alert.alert(strings.common.error, strings.exercises.nameRequired);
      return;
    }

    try {
      await updateMutation.mutateAsync(formValuesToUpdateInput(values));
      router.back();
    } catch {
      Alert.alert(strings.common.error, strings.exercises.saveFailed);
    }
  };

  const handleArchive = () => {
    Alert.alert(
      strings.exercises.archiveConfirmTitle,
      strings.exercises.archiveConfirmMessage,
      [
        { text: strings.common.cancel, style: 'cancel' },
        {
          text: strings.exercises.archiveExercise,
          style: 'destructive',
          onPress: async () => {
            try {
              await archiveMutation.mutateAsync(id ?? '');
              router.replace('/exercises');
            } catch {
              Alert.alert(strings.common.error, strings.exercises.archiveFailed);
            }
          },
        },
      ],
    );
  };

  if (isLoading || !values) {
    return (
      <ScreenContainer>
        <LoadingState message={strings.common.loading} />
      </ScreenContainer>
    );
  }

  if (isError || !exercise) {
    return (
      <ScreenContainer>
        <LoadingState message={strings.exercises.loadFailed} />
      </ScreenContainer>
    );
  }

  return (
    <ScreenContainer paddingHorizontal={false}>
      <InstructorExerciseForm
        values={values}
        onChange={setValues}
        onSubmit={handleSave}
        submitLabel={strings.common.save}
        loading={updateMutation.isPending}
        extraActions={
          <View style={styles.archiveContainer}>
            <Button
              label={strings.exercises.archiveExercise}
              variant="secondary"
              onPress={handleArchive}
              loading={archiveMutation.isPending}
            />
          </View>
        }
      />
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  archiveContainer: {
    paddingHorizontal: theme.spacing.md,
    marginTop: theme.spacing.sm,
  },
});
