import os

try:
    terminal_width = os.get_terminal_size()[0]
except OSError:
    terminal_width = 80

def final_summary(summary_dict):
    trunc('\nAll JSON files updated successfully!\n')
    for name, file_set in summary_dict.items():
        if file_set:
            status = name.replace('_', ' ')
            print(f'\nKeys {status}: {len(file_set)}')
            print('[\n' + '\n'.join(file_set) + '\n]')

def trunc(msg, end='\n'):
    truncated_lines = [
        line if len(line) < terminal_width else line[:terminal_width -4] + '...' for line in msg.splitlines() ]
    print('\n'.join(truncated_lines), end=end)
