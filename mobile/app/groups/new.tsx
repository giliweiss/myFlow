import { useState } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import {
  ScreenContainer,
  Button,
  TextField,
} from '../../src/components/ui';
import { theme } from '../../src/theme';
import { strings } from '../../src/i18n/he';

export default function NewGroupScreen() {
  const [name, setName] = useState('');
  const [level, setLevel] = useState('');
  const [duration, setDuration] = useState('');
  const [equipment, setEquipment] = useState('');
  const [limitations, setLimitations] = useState('');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);

  const handleCreate = async () => {
    setLoading(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    setLoading(false);
  };

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

          <Button
            label={strings.common.save}
            onPress={handleCreate}
            loading={loading}
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
});
