import { useMemo, useState } from 'react';
import {
  Modal,
  View,
  StyleSheet,
  ScrollView,
  Text,
  Pressable,
} from 'react-native';
import {
  TextField,
  ListItem,
  SectionHeader,
  IconButton,
  LoadingState,
  EmptyState,
} from '../ui';
import { theme } from '../../theme';
import { strings } from '../../i18n/he';
import { filterExercisesBySearch } from '../../lib/lesson-form';
import type { Exercise } from '../../types/exercise';

interface ExerciseCatalogPickerProps {
  visible: boolean;
  exercises: Exercise[];
  isLoading: boolean;
  isError: boolean;
  onClose: () => void;
  onSelectExercise: (exercise: Exercise) => void;
}

export function ExerciseCatalogPicker({
  visible,
  exercises,
  isLoading,
  isError,
  onClose,
  onSelectExercise,
}: ExerciseCatalogPickerProps) {
  const [searchText, setSearchText] = useState('');

  const filteredExercises = useMemo(
    () => filterExercisesBySearch(exercises, searchText),
    [exercises, searchText],
  );

  const handleClose = () => {
    setSearchText('');
    onClose();
  };

  const handleSelectExercise = (exercise: Exercise) => {
    onSelectExercise(exercise);
    setSearchText('');
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="pageSheet"
      onRequestClose={handleClose}
    >
      <View style={styles.container}>
        <View style={styles.header}>
          <Text style={theme.typography.title}>{strings.lessons.selectExercises}</Text>
          <Pressable onPress={handleClose} hitSlop={8}>
            <Text style={styles.closeLabel}>{strings.common.close}</Text>
          </Pressable>
        </View>

        <View style={styles.searchContainer}>
          <TextField
            label={strings.lessons.searchExercises}
            placeholder={strings.lessons.searchExercisesPlaceholder}
            value={searchText}
            onChangeText={setSearchText}
          />
        </View>

        {isLoading && (
          <LoadingState message={strings.common.loading} />
        )}

        {isError && !isLoading && (
          <EmptyState
            title={strings.common.error}
            message={strings.lessons.catalogLoadError}
            iconName="AlertCircle"
          />
        )}

        {!isLoading && !isError && filteredExercises.length === 0 && (
          <EmptyState
            title={strings.common.noData}
            message={strings.lessons.noCatalogResults}
            iconName="Search"
          />
        )}

        {!isLoading && !isError && filteredExercises.length > 0 && (
          <ScrollView contentContainerStyle={styles.listContent}>
            {filteredExercises.map((exercise) => (
              <ListItem
                key={exercise.id}
                title={exercise.name_he}
                subtitle={exercise.difficulty_level}
                iconName="Zap"
                onPress={() => handleSelectExercise(exercise)}
              />
            ))}
          </ScrollView>
        )}
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
    paddingTop: theme.spacing.lg,
  },

  header: {
    flexDirection: 'row-reverse',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: theme.spacing.md,
    marginBottom: theme.spacing.sm,
  },

  closeLabel: {
    ...theme.typography.subtitle,
    color: theme.colors.primary,
  },

  searchContainer: {
    paddingHorizontal: theme.spacing.md,
  },

  listContent: {
    paddingBottom: theme.spacing.xl,
  },
});
