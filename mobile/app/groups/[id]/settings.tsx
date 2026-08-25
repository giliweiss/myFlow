import { useEffect, useState } from 'react';
import { View, StyleSheet, ScrollView, Text } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import {
  ScreenContainer,
  Button,
  TextField,
  LoadingState,
} from '../../../src/components/ui';
import { theme } from '../../../src/theme';
import { strings } from '../../../src/i18n/he';
import { useGroup, useUpdateGroup } from '../../../src/hooks/use-groups';
import {
  formValuesToUpdatePayload,
  groupToFormValues,
} from '../../../src/lib/group-form';

export default function GroupSettingsScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams<{ id: string }>();
  const groupId = Array.isArray(id) ? id[0] : id;

  const { data: group, isLoading, isError } = useGroup(groupId);
  const updateGroup = useUpdateGroup();

  const [name, setName] = useState('');
  const [level, setLevel] = useState('');
  const [duration, setDuration] = useState('');
  const [equipment, setEquipment] = useState('');
  const [limitations, setLimitations] = useState('');
  const [notes, setNotes] = useState('');
  const [saveError, setSaveError] = useState<string | null>(null);

  useEffect(() => {
    if (group) {
      const formValues = groupToFormValues(group);
      setName(formValues.name);
      setLevel(formValues.level);
      setDuration(formValues.duration);
      setEquipment(formValues.equipment);
      setLimitations(formValues.limitations);
      setNotes(formValues.notes);
    }
  }, [group]);

  const handleSave = async () => {
    if (!groupId) {
      return;
    }

    setSaveError(null);

    try {
      await updateGroup.mutateAsync({
        groupId,
        updates: formValuesToUpdatePayload({
          name,
          level,
          duration,
          equipment,
          limitations,
          notes,
        }),
      });
      router.back();
    } catch {
      setSaveError(strings.common.error);
    }
  };

  if (isLoading) {
    return (
      <ScreenContainer>
        <LoadingState message={strings.common.loading} />
      </ScreenContainer>
    );
  }

  if (isError || !group) {
    return (
      <ScreenContainer>
        <LoadingState message={strings.common.error} />
      </ScreenContainer>
    );
  }

  return (
    <ScreenContainer paddingHorizontal={false}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.container}>
          <TextField
            label={strings.groups.groupName}
            placeholder="שם הקבוצה"
            value={name}
            onChangeText={setName}
          />
          <TextField
            label={strings.groups.groupLevel}
            placeholder="בינוני / מתחיל / מתקדם"
            value={level}
            onChangeText={setLevel}
          />
          <TextField
            label={strings.groups.typicalDuration}
            placeholder="45"
            value={duration}
            onChangeText={setDuration}
          />
          <TextField
            label={strings.groups.equipment}
            placeholder="מחצלת, כדור, טבעת"
            value={equipment}
            onChangeText={setEquipment}
          />
          <TextField
            label={strings.groups.limitations}
            placeholder="אין קפיצות, גב חלש"
            value={limitations}
            onChangeText={setLimitations}
          />
          <TextField
            label={strings.groups.notes}
            placeholder="הערות נוספות"
            value={notes}
            onChangeText={setNotes}
            multiline
            numberOfLines={3}
          />

          {saveError ? (
            <Text style={styles.errorText}>{saveError}</Text>
          ) : null}

          <Button
            label={strings.common.save}
            onPress={handleSave}
            loading={updateGroup.isPending}
            style={styles.submitButton}
          />
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  scrollContent: {
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.md,
  },

  container: {
    flex: 1,
  },

  submitButton: {
    marginTop: theme.spacing.lg,
    marginBottom: theme.spacing.lg,
  },

  errorText: {
    ...theme.typography.caption,
    color: theme.colors.error,
    marginTop: theme.spacing.sm,
    textAlign: 'right',
  },
});
