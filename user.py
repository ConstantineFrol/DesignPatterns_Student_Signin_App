from datetime import datetime


def _get_registration_date():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


class User:
    def __init__(self, user_id, user_name, attendance_qty, user_role, img_encode):
        self.t_number = user_id
        self.name = user_name
        self.registration_date = _get_registration_date()
        self.total_attendance = attendance_qty
        self.role = user_role
        self.encode = img_encode

    def __str__(self):
        return f"User Info:\n\
                t_number: {self.t_number}\n\
                name: {self.name}\n\
                registered: {self.registration_date}\n\
                total_attendance: {self.total_attendance}\n\
                role: {self.role}\n\
                encode: {self.encode}"


# Test
t_number = 't00123456'
name = 'lol'
total_attendance = 5
role = 'student'
encode = '-0.21615925431251526, 0.08906067907810211, 0.0018564686179161072, -0.08332519978284836, -0.1646469682455063, 0.03232419863343239, 0.023419342935085297, -0.12622202932834625, 0.13024744391441345, -0.002603699453175068, 0.18917237222194672, -0.004828600212931633, -0.2775905430316925, -0.05119749531149864, 0.021721214056015015, 0.011727537959814072, -0.1253194957971573, -0.0972324088215828, -0.06749843806028366, -0.08160320669412613, 0.04920903593301773, 0.038717109709978104, 0.007090273778885603, 0.14121781289577484, -0.11687357723712921, -0.22418496012687683, -0.05252625048160553, -0.10761841386556625, -0.011875427328050137, -0.05987859144806862, 0.0976705327630043, 0.04407956451177597, -0.15515825152397156, -0.07346691936254501, 0.04035007581114769, 0.1349416971206665, -0.06972178816795349, 0.01217928808182478, 0.24537913501262665, -0.0798904150724411, -0.1687501221895218, -0.024633925408124924, 0.09950705617666245, 0.2965802252292633, 0.11979065090417862, 0.011406470090150833, -0.03215418756008148, -0.06997708976268768, 0.14997321367263794, -0.24490098655223846, 0.04464743286371231, 0.2422584891319275, 0.16076844930648804, -0.005408794619143009, 0.05336500331759453, -0.14606745541095734, 0.06687329709529877, 0.16665859520435333, -0.2479812502861023, 0.11839871108531952, 0.08610852062702179, -0.1908375769853592, 0.00885256938636303, -0.05641091242432594, 0.24182207882404327, 0.07803782820701599, -0.167024165391922, -0.1437130719423294, 0.03772711008787155, -0.11959969997406006, -0.09532937407493591, 0.16419333219528198, -0.13480140268802643, -0.22648613154888153, -0.27747613191604614, 0.10345812141895294, 0.5234206914901733, 0.11002027243375778, -0.1771019697189331, 0.05578065663576126, -0.15738555788993835, -0.07992935180664062, 0.05349172651767731, 0.092094786465168, -0.08992154151201248, -0.0855579525232315, -0.13462987542152405, 0.03887074440717697, 0.17472489178180695, -0.02180783450603485, -0.028732240200042725, 0.2005225270986557, 0.06702068448066711, 0.024175450205802917, 0.02856636792421341, 0.06408116221427917, -0.13939934968948364, -0.001922669354826212, -0.09207300841808319, 0.002914424054324627, 0.0036280276253819466, -0.13915468752384186, 0.08169784396886826, 0.023954693228006363, -0.21461020410060883, 0.16874440014362335, 0.03641815111041069, -0.05037488788366318, -0.03730753809213638, -0.06891880929470062, -0.14318010210990906, -0.00039841397665441036, 0.1965753585100174, -0.35871440172195435, 0.24639646708965302, 0.08785979449748993, 0.044990040361881256, 0.20308715105056763, 0.10860300064086914, 0.07728153467178345, 0.00786583125591278, 0.0077084871008992195, -0.04643022269010544, -0.06467413902282715, 0.1078193187713623, -0.04806381091475487, 0.15488766133785248, 0.012902794405817986'

user = User(t_number, name, total_attendance, role, encode)

# Print user information
print(user)
