sudo apt install zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

mkdir .ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCwkyHiRw7sHi6gazwaiRAS/vA3phjlfxyyoPNBkmirEuc6ey5RaDnxUESNch7JiPWpSb2ZFHbfmxxvJCJmlf3LylOZHXWkssBTo3ITX1Bv9ZW9G0SF868oDe/L0ZyL5kACm9R2DpmOv+XKdX+o2k7W612qYHh1e29hj1LAtZWF3FDY71EPTWVsOe2REgiau4cbZwNQAvn9b07IcCQsdH+4870VHyHB33uHx1DNEzJ57gE+qu3klzDF98gKmHSR7AteeZqBCWZJo8kTrBayimrCNDUjJflCMykqSrnhlrU1UICtyOo9KTrerXXVJ4NLignghN4Ee9LCMU0Fo2dlCqdpiziXfOuE72Lr3kPa7Hd0y+EB1fuM/ZXu7M0IMiY4zDQ5SoSFnvvnGRWNuhA8ShiG8f3ZeIK2HLEQtDW0W7m3ctYL+gTxwGUtFpjMnGGXkuhVYEp3EULmBypNgTV8C0yLP3ip5YcQ1s3R4gD9DP5DKSn+jFmh4zFpi2AjYi7c9pc=" >> ~/.ssh/authorized_keys


pip install psycopg2-binary

sudo apt update
sudo apt install libpq-dev python3-dev
