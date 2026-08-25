import { View, StyleSheet, Text } from 'react-native';
import { ListItem, SectionHeader, IconButton } from '../ui';
import { theme } from '../../theme';
import { strings } from '../../i18n/he';
import type { BuilderExercise, LessonSection } from '../../types/lesson';

const SECTION_LABELS: Record<LessonSection, string> = {
  warmup: strings.lessons.warmup,
  main: strings.lessons.main,
  cooldown: strings.lessons.cooldown,
};

const SECTIONS: LessonSection[] = ['warmup', 'main', 'cooldown'];

interface LessonBuilderProps {
  exercises: BuilderExercise[];
  onAddExercise: (section: LessonSection) => void;
  onRemoveExercise: (localId: string) => void;
  onMoveExercise: (localId: string, direction: 'up' | 'down') => void;
  editable?: boolean;
}

export function LessonBuilder({
  exercises,
  onAddExercise,
  onRemoveExercise,
  onMoveExercise,
  editable = true,
}: LessonBuilderProps) {
  const renderSection = (section: LessonSection) => {
    const sectionExercises = exercises.filter((item) => item.section === section);

    return (
      <View key={section} style={styles.section}>
        <SectionHeader
          title={SECTION_LABELS[section]}
          action={
            editable ? (
              <IconButton
                iconName="Plus"
                onPress={() => onAddExercise(section)}
                size={20}
                color={theme.colors.primary}
              />
            ) : undefined
          }
        />

        {sectionExercises.map((exercise, index) => (
          <View key={exercise.localId} style={styles.exerciseRow}>
            <ListItem
              title={exercise.nameHe}
              iconName="Zap"
              rightContent={
                editable ? (
                  <View style={styles.rowActions}>
                    <IconButton
                      iconName="ChevronUp"
                      onPress={() => onMoveExercise(exercise.localId, 'up')}
                      size={18}
                      color={theme.colors.textSecondary}
                      disabled={index === 0}
                    />
                    <IconButton
                      iconName="ChevronDown"
                      onPress={() => onMoveExercise(exercise.localId, 'down')}
                      size={18}
                      color={theme.colors.textSecondary}
                      disabled={index === sectionExercises.length - 1}
                    />
                    <IconButton
                      iconName="Trash2"
                      onPress={() => onRemoveExercise(exercise.localId)}
                      size={18}
                      color={theme.colors.error}
                    />
                  </View>
                ) : undefined
              }
            />
          </View>
        ))}

        {sectionExercises.length === 0 && (
          <Text style={[theme.typography.caption, styles.emptyText]}>
            {strings.lessons.noExercises}
          </Text>
        )}
      </View>
    );
  };

  return (
    <View style={styles.container}>
      {SECTIONS.map(renderSection)}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginTop: theme.spacing.md,
  },

  section: {
    marginBottom: theme.spacing.lg,
  },

  exerciseRow: {
    backgroundColor: theme.colors.surface,
  },

  rowActions: {
    flexDirection: 'row-reverse',
    alignItems: 'center',
  },

  emptyText: {
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.md,
    textAlign: 'right',
  },
});
