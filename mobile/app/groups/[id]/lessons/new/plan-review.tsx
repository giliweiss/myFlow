import { useEffect, useMemo, useState } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import {
  Button,
  LoadingState,
  ScreenContainer,
} from '../../../../../src/components/ui';
import { theme } from '../../../../../src/theme';
import { strings } from '../../../../../src/i18n/he';
import { useExerciseCatalog } from '../../../../../src/hooks/use-exercises';
import {
  consumeLessonPlanReviewDraft,
  setLessonBuilderDraft,
  type LessonPlanReviewDraft,
} from '../../../../../src/lib/lesson-draft';
import type { LessonSection } from '../../../../../src/types/lesson';

const SECTION_ORDER: LessonSection[] = ['warmup', 'main', 'cooldown'];

export default function PlanReviewScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const groupId = Array.isArray(id) ? id[0] : id;
  const { data: catalogExercises = [] } = useExerciseCatalog();
  const [draft, setDraft] = useState<LessonPlanReviewDraft | null>(null);

  useEffect(() => {
    setDraft(consumeLessonPlanReviewDraft());
  }, []);

  const exercisesBySection = useMemo(() => {
    if (!draft) {
      return {
        warmup: [],
        main: [],
        cooldown: [],
      };
    }

    return SECTION_ORDER.reduce(
      (sections, section) => {
        sections[section] = draft.builderDraft.exercises.filter(
          (exercise) => exercise.section === section,
        );
        return sections;
      },
      {
        warmup: [],
        main: [],
        cooldown: [],
      } as Record<LessonSection, typeof draft.builderDraft.exercises>,
    );
  }, [draft]);

  const getExerciseName = (exerciseId: string) => {
    const exercise = catalogExercises.find((item) => item.id === exerciseId);
    return exercise?.name_he || exercise?.name_en || exerciseId;
  };

  if (!draft) {
    return (
      <ScreenContainer>
        <LoadingState message={strings.common.loading} />
      </ScreenContainer>
    );
  }

  const handleOpenBuilder = () => {
    setLessonBuilderDraft(draft.builderDraft);
    router.replace(`/groups/${groupId}/lessons/new/manual`);
  };

  const handleAdjustIntention = () => {
    router.replace(`/groups/${groupId}/lessons/new/ai`);
  };

  const handleStartOver = () => {
    router.replace(`/groups/${groupId}/lessons/new/ai`);
  };

  return (
    <ScreenContainer paddingHorizontal={false}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Text style={[theme.typography.title, styles.title]}>{draft.title}</Text>
        <Text style={[theme.typography.body, styles.subtitle]}>
          {draft.primaryGoal}
        </Text>

        <View style={styles.card}>
          <Text style={[theme.typography.subtitle, styles.cardTitle]}>
            {strings.lessons.planReviewStrategy}
          </Text>
          {draft.guidance.lesson_strategy ? (
            <Text style={styles.cardText}>{draft.guidance.lesson_strategy}</Text>
          ) : null}
          {draft.guidance.structure_rationale ? (
            <Text style={styles.cardText}>{draft.guidance.structure_rationale}</Text>
          ) : null}
          {draft.guidance.progression_logic ? (
            <Text style={styles.cardText}>{draft.guidance.progression_logic}</Text>
          ) : null}
        </View>

        {SECTION_ORDER.map((section) => {
          const sectionExercises = exercisesBySection[section] || [];
          if (sectionExercises.length === 0) {
            return null;
          }

          return (
            <View key={section} style={styles.card}>
              <Text style={[theme.typography.subtitle, styles.cardTitle]}>
                {strings.lessons[section]}
              </Text>
              {sectionExercises.map((exercise) => (
                <Text key={exercise.localId} style={styles.exerciseLine}>
                  {exercise.nameHe || getExerciseName(exercise.exerciseId)}
                </Text>
              ))}
            </View>
          );
        })}

        <Button
          label={strings.lessons.openInBuilder}
          onPress={handleOpenBuilder}
          style={styles.primaryButton}
        />
        <Button
          label={strings.lessons.adjustIntention}
          onPress={handleAdjustIntention}
          variant="secondary"
          style={styles.secondaryButton}
        />
        <Button
          label={strings.lessons.startOver}
          onPress={handleStartOver}
          variant="secondary"
        />
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  scrollContent: {
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.md,
  },

  title: {
    textAlign: 'right',
    marginBottom: theme.spacing.xs,
  },

  subtitle: {
    textAlign: 'right',
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.lg,
  },

  card: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.radius.md,
    padding: theme.spacing.md,
    marginBottom: theme.spacing.md,
  },

  cardTitle: {
    textAlign: 'right',
    marginBottom: theme.spacing.sm,
  },

  cardText: {
    textAlign: 'right',
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.sm,
  },

  exerciseLine: {
    textAlign: 'right',
    marginBottom: theme.spacing.xs,
  },

  primaryButton: {
    marginTop: theme.spacing.md,
    marginBottom: theme.spacing.sm,
  },

  secondaryButton: {
    marginBottom: theme.spacing.sm,
  },
});
