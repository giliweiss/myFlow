import { useState } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import {
  ScreenContainer,
  Card,
  Button,
  TextField,
} from '../../../../../src/components/ui';
import { theme } from '../../../../../src/theme';
import { strings } from '../../../../../src/i18n/he';

export default function AddReviewScreen() {
  const [rating, setRating] = useState('4');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
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
          <Card style={styles.card}>
            <TextField
              label="דירוג (1-5)"
              placeholder="4"
              value={rating}
              onChangeText={setRating}
            />
            <TextField
              label="הערות"
              placeholder="כתוב הערות על השיעור..."
              value={notes}
              onChangeText={setNotes}
              multiline
              numberOfLines={5}
            />
          </Card>

          <Button
            label={strings.common.save}
            onPress={handleSubmit}
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
    flexGrow: 1,
  },

  container: {
    flex: 1,
  },

  card: {
    marginBottom: theme.spacing.lg,
  },

  submitButton: {
    marginTop: theme.spacing.lg,
  },
});
