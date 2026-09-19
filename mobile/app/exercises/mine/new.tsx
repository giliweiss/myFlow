import { useState } from 'react';
import { Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { ScreenContainer } from '../../../src/components/ui';
import { InstructorExerciseForm } from '../../../src/components/exercise/InstructorExerciseForm';
import { strings } from '../../../src/i18n/he';
import { useCreateInstructorExercise } from '../../../src/hooks/use-instructor-exercises';
import {
  formValuesToCreateInput,
  type InstructorExerciseFormValues,
} from '../../../src/lib/instructor-exercise-form';

const emptyFormValues: InstructorExerciseFormValues = {
  nameHe: '',
  nameEn: '',
  descriptionHe: '',
  level: 'בינוני',
  bodyFocus: '',
  equipment: '',
  teachingNotes: '',
};

export default function NewInstructorExerciseScreen() {
  const router = useRouter();
  const [values, setValues] = useState<InstructorExerciseFormValues>(emptyFormValues);
  const createMutation = useCreateInstructorExercise();

  const handleSave = async () => {
    if (!values.nameHe.trim()) {
      Alert.alert(strings.common.error, strings.exercises.nameRequired);
      return;
    }

    try {
      const exercise = await createMutation.mutateAsync(formValuesToCreateInput(values));
      router.replace(`/exercises/mine/${exercise.id}`);
    } catch {
      Alert.alert(strings.common.error, strings.exercises.saveFailed);
    }
  };

  return (
    <ScreenContainer paddingHorizontal={false}>
      <InstructorExerciseForm
        values={values}
        onChange={setValues}
        onSubmit={handleSave}
        submitLabel={strings.common.save}
        loading={createMutation.isPending}
      />
    </ScreenContainer>
  );
}
