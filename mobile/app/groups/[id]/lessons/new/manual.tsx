import { useEffect, useState } from 'react';
import { View, StyleSheet, ScrollView, Text, Alert } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import {
  ScreenContainer,
  TextField,
  Button,
  LoadingState,
} from '../../../../../src/components/ui';
import { LessonBuilder } from '../../../../../src/components/lesson/LessonBuilder';
import { ExerciseCatalogPicker } from '../../../../../src/components/lesson/ExerciseCatalogPicker';
import { theme } from '../../../../../src/theme';
import { strings } from '../../../../../src/i18n/he';
import { useGroup } from '../../../../../src/hooks/use-groups';
import { useExerciseCatalog } from '../../../../../src/hooks/use-exercises';
import { useCreateLesson } from '../../../../../src/hooks/use-lessons';
import {
  addExerciseToSection,
  buildCreateLessonInput,
  findExercisesWithLevelMismatch,
  moveExerciseInSection,
  parseDateInputToIso,
  removeBuilderExercise,
  todayDateInput,
} from '../../../../../src/lib/lesson-form';
import { levelToDisplay } from '../../../../../src/lib/group-form';
import type { BuilderExercise, LessonSection } from '../../../../../src/types/lesson';

export default function ManualBuildLessonScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const groupId = Array.isArray(id) ? id[0] : id;

  const { data: group, isLoading: isGroupLoading } = useGroup(groupId);
  const {
    data: catalogExercises = [],
    isLoading: isCatalogLoading,
    isError: isCatalogError,
  } = useExerciseCatalog();
  const createLesson = useCreateLesson(groupId);

  const [title, setTitle] = useState('');
  const [primaryGoal, setPrimaryGoal] = useState('');
  const [notes, setNotes] = useState('');
  const [duration, setDuration] = useState('');
  const [scheduledDate, setScheduledDate] = useState(todayDateInput());

  useEffect(() => {
    if (group?.typical_duration_minutes) {
      setDuration((current) => current || String(group.typical_duration_minutes));
    }
  }, [group?.typical_duration_minutes]);
  const [exercises, setExercises] = useState<BuilderExercise[]>([]);
  const [pickerSection, setPickerSection] = useState<LessonSection | null>(null);
  const [titleError, setTitleError] = useState('');
  const [dateError, setDateError] = useState('');

  const plannedDurationMinutes =
    Number(duration) || group?.typical_duration_minutes || 45;

  const handleOpenPicker = (section: LessonSection) => {
    setPickerSection(section);
  };

  const handleClosePicker = () => {
    setPickerSection(null);
  };

  const handleSelectExercise = (exercise: (typeof catalogExercises)[number]) => {
    if (!pickerSection) {
      return;
    }
    setExercises((current) => addExerciseToSection(current, exercise, pickerSection));
    setPickerSection(null);
  };

  const performSave = async () => {
    try {
      const lesson = await createLesson.mutateAsync(
        buildCreateLessonInput({
          title,
          primaryGoal,
          notes,
          plannedDurationMinutes,
          scheduledDate,
          exercises,
        }),
      );

      router.replace(`/groups/${groupId}/lessons/${lesson.id}`);
    } catch {
      Alert.alert(strings.common.error, strings.lessons.saveFailed);
    }
  };

  const handleSave = () => {
    if (!title.trim()) {
      setTitleError(strings.lessons.titleRequired);
      return;
    }

    if (!parseDateInputToIso(scheduledDate)) {
      setDateError(strings.lessons.dateInvalid);
      return;
    }

    if (!group) {
      return;
    }

    setTitleError('');
    setDateError('');

    const levelMismatchNames = findExercisesWithLevelMismatch(
      exercises,
      catalogExercises,
      group.level,
    );

    if (levelMismatchNames.length > 0) {
      const message = strings.lessons.levelMismatchMessage
        .replace('{groupLevel}', levelToDisplay(group.level))
        .replace('{exerciseNames}', levelMismatchNames.join(', '));

      Alert.alert(strings.lessons.levelMismatchTitle, message, [
        { text: strings.common.cancel, style: 'cancel' },
        { text: strings.lessons.saveAnyway, onPress: performSave },
      ]);
      return;
    }

    void performSave();
  };

  if (isGroupLoading || !group) {
    return (
      <ScreenContainer>
        <LoadingState message={strings.common.loading} />
      </ScreenContainer>
    );
  }

  return (
    <ScreenContainer paddingHorizontal={false}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
      >
        <TextField
          label={strings.lessons.lessonTitle}
          placeholder={strings.lessons.lessonTitle}
          value={title}
          onChangeText={(value) => {
            setTitle(value);
            if (titleError) {
              setTitleError('');
            }
          }}
          error={titleError}
        />

        <TextField
          label={strings.lessons.primaryGoal}
          placeholder={strings.lessons.primaryGoal}
          value={primaryGoal}
          onChangeText={setPrimaryGoal}
        />

        <TextField
          label={strings.lessons.lessonDate}
          placeholder={strings.lessons.lessonDatePlaceholder}
          value={scheduledDate}
          onChangeText={(value) => {
            setScheduledDate(value);
            if (dateError) {
              setDateError('');
            }
          }}
          error={dateError}
        />

        <TextField
          label={strings.lessons.duration}
          placeholder={String(group.typical_duration_minutes)}
          value={duration}
          onChangeText={setDuration}
        />

        <TextField
          label={strings.lessons.lessonNotes}
          placeholder={strings.lessons.lessonNotes}
          value={notes}
          onChangeText={setNotes}
          multiline
          numberOfLines={4}
        />

        <Text style={[theme.typography.subtitle, styles.exercisesLabel]}>
          {strings.lessons.exercises}
        </Text>

        <LessonBuilder
          exercises={exercises}
          onAddExercise={handleOpenPicker}
          onRemoveExercise={(localId) =>
            setExercises((current) => removeBuilderExercise(current, localId))
          }
          onMoveExercise={(localId, direction) =>
            setExercises((current) => moveExerciseInSection(current, localId, direction))
          }
        />

        <Button
          label={strings.common.save}
          onPress={handleSave}
          loading={createLesson.isPending}
          style={styles.submitButton}
        />
      </ScrollView>

      <ExerciseCatalogPicker
        visible={pickerSection !== null}
        exercises={catalogExercises}
        isLoading={isCatalogLoading}
        isError={isCatalogError}
        onClose={handleClosePicker}
        onSelectExercise={handleSelectExercise}
      />
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  scrollContent: {
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.md,
  },

  exercisesLabel: {
    textAlign: 'right',
    marginBottom: theme.spacing.sm,
  },

  submitButton: {
    marginTop: theme.spacing.lg,
    marginBottom: theme.spacing.lg,
  },
});
