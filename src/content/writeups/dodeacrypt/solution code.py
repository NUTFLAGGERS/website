# DodecaCrypt Cyclic Constraint Engine (Flag Image Version)

# 1. Color mapping to the User's exact letter codes
COLOR_CODES = {
    'Red': 'A', 'Yellow': 'C', 'Cyan': 'G', 'Dark Pink': 'H', 
    'Lime Green': 'I', 'Light Purple': 'L', 'Brown': 'O', 
    'Light Green': 'P', 'Beige': 'R', 'Dark Blue': 'S', 
    'Dark Green': 'X', 'Purple': 'Y'
}

# 2. The exact mathematical geometry (b, c, d, e, f in cyclic order from your spreadsheet)
rules = {
    1: [2, 6, 4, 5, 3],
    2: [1, 3, 10, 7, 6],
    3: [1, 5, 9, 10, 2],
    4: [1, 6, 8, 11, 5],
    5: [1, 4, 11, 9, 3],
    6: [1, 2, 7, 8, 4],
    7: [2, 10, 12, 8, 6],
    8: [4, 6, 7, 12, 11],
    9: [3, 5, 11, 12, 10],
    10: [2, 3, 9, 12, 7],
    11: [4, 8, 12, 9, 5],
    12: [7, 10, 9, 11, 8]
}

# 3. The exact shapes extracted from flag.jpg / image_fe508a.jpg
# Format: ('Center_Color', ['Outer_1', 'Outer_2', 'Outer_3', 'Outer_4', 'Outer_5'])
# Note: Listed in clockwise order. If a shape fails, double check these for visual shading errors!
observed_shapes = [
    ('Purple',       ['Dark Green', 'Light Purple', 'Lime Green', 'Red', 'Beige']),
    ('Brown',        ['Cyan', 'Yellow', 'Light Green' , 'Beige', 'Dark Green']),
    ('Brown',        ['Beige', 'Light Green', 'Yellow' , 'Cyan', 'Dark Green']),
    ('Light Green',  ['Dark Blue', 'Yellow', 'Brown', 'Beige', 'Red']),
    ('Red',          ['Dark Blue', 'Lime Green', 'Purple', 'Beige', 'Light Green']),
    ('Lime Green',   ['Red', 'Dark Blue',  'Dark Pink', 'Light Purple', 'Purple']),
    ('Light Purple', ['Lime Green', 'Purple', 'Dark Green', 'Cyan', 'Dark Pink']),
    ('Yellow',       ['Cyan', 'Brown', 'Light Green', 'Dark Blue', 'Dark Pink']),
    ('Beige',        ['Purple',  'Dark Green', 'Brown',  'Light Green', 'Red']),
    ('Dark Pink',    ['Yellow', 'Dark Blue', 'Lime Green', 'Light Purple', 'Cyan'])
]

colors = list(COLOR_CODES.keys())
numbers = set(range(1, 13))
solutions = []

def get_all_rotations(sequence):
    """Returns all 5 valid clockwise rotations of the outer ring."""
    return [sequence[i:] + sequence[:i] for i in range(len(sequence))]

def solve_matrix(mapping, remaining_colors, remaining_numbers):
    if not remaining_colors:
        solutions.append(mapping.copy())
        return

    c = remaining_colors[0]
    for n in list(remaining_numbers):
        valid = True
        mapping[c] = n
        
        # Check all currently mapped shapes for cyclic validity
        for obs_center, obs_outers in observed_shapes:
            if obs_center in mapping:
                center_num = mapping[obs_center]
                rule_sequence = rules[center_num]
                
                # EARLY PRUNING: Immediately reject if any mapped outer color isn't in the rule sequence
                for outer_c in obs_outers:
                    if outer_c in mapping and mapping[outer_c] not in rule_sequence:
                        valid = False
                        break
                
                if not valid:
                    break
                
                # FULL CYCLIC CHECK: Only run if all outer colors are currently mapped
                if all(outer_c in mapping for outer_c in obs_outers):
                    mapped_outers = [mapping[outer_c] for outer_c in obs_outers]
                    
                    valid_rotations = get_all_rotations(rule_sequence)
                    flipped_rotations = get_all_rotations(rule_sequence[::-1])
                    
                    if mapped_outers not in valid_rotations and mapped_outers not in flipped_rotations:
                        valid = False
                        break
                        
        if valid:
            remaining_numbers.remove(n)
            solve_matrix(mapping, remaining_colors[1:], remaining_numbers)
            remaining_numbers.add(n)
            
        del mapping[c]

print("Running Cyclic Constraint Engine...")
solve_matrix({}, colors, numbers)

if len(solutions) > 0:
    print(f"\nSUCCESS! Found Secret Key Mapping:")
    sorted_key = sorted(solutions[0].items(), key=lambda item: item[1])
    for color, slot in sorted_key:
        print(f"Key Slot {slot}: {color} (Code {COLOR_CODES[color]})")
else:
    print("\nFAILED: 0 solutions found. Check the `observed_shapes` list for shading misidentifications.")