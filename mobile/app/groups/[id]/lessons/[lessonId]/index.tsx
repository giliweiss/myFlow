import { useEffect, useState } from 'react';
import { View, StyleSheet, ScrollView, Text, Alert } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import {
  ScreenContainer,
  TextField,
  Button,
  LoadingState,
} from '../../../../../src/components/ui';
import { LessonBuilder } from '../../../../../src/components/lesson/LessonBuilder';
import { ExerciseCatalogPicker } from '../../../../../src/components/lesson/ExerciseCatalogPicker';
import { StatusPicker } from '../../../../../src/components/lesson/StatusPicker';
import { theme } from '../../../../../src/theme';
import { strings } from '../../../../../src/i18n/he';
import { useGroup } from '../../../../../src/hooks/use-groups';
import { useExerciseCatalog } from '../../../../../src/hooks/use-exercises';
import { useLesson, useUpdateLesson } from '../../../../../src/hooks/use-lessons';
import {
  addExerciseToSection,
  buildUpdateLessonInput,
  findExercisesWithLevelMismatch,
  lessonToFormState,
  moveExerciseInSection,
  parseDateInputToIso,
  removeBuilderExercise,
} from '../../../../../src/lib/lesson-form';
import { levelToDisplay } from '../../../../../src/lib/group-form';
import {
  getSelectableStatuses,
  isLessonEditable,
  normalizeLessonStatus,
  STATUS_LABELS,
  STATUS_VARIANTS,
} from '../../../../../src/lib/lesson-status';
import { Badge } from '../../../../../src/components/ui';
import type { BuilderExercise, LessonSection, LessonStatus } from '../../../../../src/types/lesson';

export default function LessonDetailScreen() {
  const { id, lessonId: lessonIdParam } = useLocalSearchParams<{
    id: string;
    lessonId: string;
  }>();
  const groupId = Array.isArray(id) ? id[0] : id;
  const lessonId = Array.isArray(lessonIdParam) ? lessonIdParam[0] : lessonIdParam;

  const { data: lesson, isLoading, isError } = useLesson(lessonId);
  const { data: group } = useGroup(groupId);
  const {
    data: catalogExercises = [],
    isLoading: isCatalogLoading,
    isError: isCatalogError,
  } = useExerciseCatalog();
  const updateLesson = useUpdateLesson(lessonId);

  const [title, setTitle] = useState('');
  const [primaryGoal, setPrimaryGoal] = useState('');
  const [notes, setNotes] = useState('');
  const [duration, setDuration] = useState('');
  const [scheduledDate, setScheduledDate] = useState('');
  const [status, setStatus] = useState<LessonStatus>('upcoming');
  const [exercises, setExercises] = useState<BuilderExercise[]>([]);
  const [pickerSection, setPickerSection] = useState<LessonSection | null>(null);
  const [titleError, setTitleError] = useState('');
  const [dateError, setDateError] = useState('');
  const [isFormInitialized, setIsFormInitialized] = useState(false);

  useEffect(() => {
    setIsFormInitialized(false);
  }, [lessonId]);

  useEffect(() => {
    if (!lesson || isFormInitialized) {
      return;
    }

    if (lesson.lesson_exercises.length > 0 && catalogExercises.length === 0) {
      return;
    }

    const formState = lessonToFormState(lesson, catalogExercises);
    setTitle(formState.title);
    setPrimaryGoal(formState.primaryGoal);
    setNotes(formState.notes);
    setDuration(formState.duration);
    setScheduledDate(formState.scheduledDate);
    setStatus(formState.status);
    setExercises(formState.exercises);
    setIsFormInitialized(true);
  }, [lesson, catalogExercises, isFormInitialized]);

  const editable = lesson ? isLessonEditable(normalizeLessonStatus(lesson.status)) : false;
  const plannedDurationMinutes =
    Number(duration) || lesson?.planned_duration_minutes || 45;

  const performSave = async () => {
    try {
      await updateLesson.mutateAsync(
        buildUpdateLessonInput({
          title,
          primaryGoal,
          notes,
          plannedDurationMinutes,
          scheduledDate,
          status,
          exercises,
        }),
      );
    } catch {
      Alert.alert(strings.common.error, strings.lessons.updateFailed);
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

  if (isLoading || !lesson || !isFormInitialized) {
    return (
      <ScreenContainer>
        <LoadingState message={strings.common.loading} />
      </ScreenContainer>
    );
  }

  if (isError) {
    return (
      <ScreenContainer>
        <LoadingState message={strings.common.error} />
      </ScreenContainer>
    );
  }

  const statusOptions = getSelectableStatuses(normalizeLessonStatus(lesson.status));

  return (
    <ScreenContainer paddingHorizontal={false}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
      >
        {!editable && (
          <Text style={[theme.typography.body, styles.readOnlyNotice]}>
            {strings.lessons.lessonNotEditable}
          </Text>
        )}

        <View style={styles.statusRow}>
          <Text style={theme.typography.subtitle}>{strings.lessons.status}</Text>
          {editable ? (
            <StatusPicker
              value={status}
              options={statusOptions}
              onChange={setStatus}
            />
          ) : (
            <Badge
              label={STATUS_LABELS[normalizeLessonStatus(lesson.status)]}
              variant={STATUS_VARIANTS[normalizeLessonStatus(lesson.status)]}
            />
          )}
        </View>

        <TextField
          label={strings.lessons.lessonTitle}
          placeholder={strings.lessons.lessonTitle}
          value={title}
          editable={editable}
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
          editable={editable}
          onChangeText={setPrimaryGoal}
        />

        <TextField
          label={strings.lessons.lessonDate}
          placeholder={strings.lessons.lessonDatePlaceholder}
          value={scheduledDate}
          editable={editable}
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
          placeholder={String(lesson.planned_duration_minutes ?? '')}
          value={duration}
          editable={editable}
          onChangeText={setDuration}
        />

        <TextField
          label={strings.lessons.lessonNotes}
          placeholder={strings.lessons.lessonNotes}
          value={notes}
          editable={editable}
          onChangeText={setNotes}
          multiline
          numberOfLines={4}
        />

        <Text style={[theme.typography.subtitle, styles.exercisesLabel]}>
          {strings.lessons.exercises}
        </Text>

        <LessonBuilder
          exercises={exercises}
          editable={editable}
          onAddExercise={(section) => setPickerSection(section)}
          onRemoveExercise={(localId) =>
            setExercises((current) => removeBuilderExercise(current, localId))
          }
          onMoveExercise={(localId, direction) =>
            setExercises((current) => moveExerciseInSection(current, localId, direction))
          }
        />

        {editable && (
          <Button
            label={strings.common.save}
            onPress={handleSave}
            loading={updateLesson.isPending}
            style={styles.submitButton}
          />
        )}
      </ScrollView>

      {editable && (
        <ExerciseCatalogPicker
          visible={pickerSection !== null}
          exercises={catalogExercises}
          isLoading={isCatalogLoading}
          isError={isCatalogError}
          onClose={() => setPickerSection(null)}
          onSelectExercise={(exercise) => {
            if (!pickerSection) {
              return;
            }
            setExercises((current) =>
              addExerciseToSection(current, exercise, pickerSection),
            );
            setPickerSection(null);
          }}
        />
      )}
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  scrollContent: {
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.md,
  },

  readOnlyNotice: {
    textAlign: 'right',
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.md,
  },

  statusRow: {
    marginBottom: theme.spacing.lg,
    alignItems: 'flex-end',
    gap: theme.spacing.sm,
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
